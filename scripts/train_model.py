import pandas as pd
import numpy as np
import tensorflow as tf
import keras_tuner as kt
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from pathlib import Path
import logging
import sys

# ---------------------------------------------------
# 1. SETUP & CONFIGURATION
# ---------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("DeepLearning")

ARTIFACT_DIR = Path("../artifacts_nn")
ARTIFACT_DIR.mkdir(exist_ok=True)

DATA_PATH = "../dataset/train.csv"
RAW_TARGET = "Heart Disease"  # The name as it appears in CSV


# ---------------------------------------------------
# 2. UTILITY: DATAFRAME TO DATASET
# ---------------------------------------------------
def df_to_dataset(dataframe, target_col, shuffle=True, batch_size=32):
    df = dataframe.copy()
    labels = df.pop(target_col)
    ds = tf.data.Dataset.from_tensor_slices((dict(df), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size).cache().prefetch(tf.data.AUTOTUNE)
    return ds


# ---------------------------------------------------
# 3. THE HYPERMODEL CLASS
# ---------------------------------------------------
class HeartDiseaseHyperModel(kt.HyperModel):
    def __init__(self, train_df, numeric_cols, categorical_cols):
        self.train_df = train_df
        self.numeric_cols = numeric_cols
        self.categorical_cols = categorical_cols
        self.stats = {}
        self.vocabs = {}
        self._calculate_stats()

    def _calculate_stats(self):
        logger.info("Pre-calculating dataset statistics...")
        # Numeric Stats
        for col in self.numeric_cols:
            self.stats[col] = {
                'mean': np.array(self.train_df[col].mean()),
                'var': np.array(self.train_df[col].var())
            }
        # String Vocabularies
        for col in self.categorical_cols:
            unique_vals = self.train_df[col].astype(str).unique()
            self.vocabs[col] = unique_vals.tolist()

    def build(self, hp):
        inputs = {}
        all_features = []

        # 1. Numeric Inputs
        for name in self.numeric_cols:
            inputs[name] = keras.Input(shape=(1,), name=name, dtype='float32')
            norm = layers.Normalization(
                mean=self.stats[name]['mean'],
                variance=self.stats[name]['var'],
                name=f'norm_{name}'
            )
            x = norm(inputs[name])
            all_features.append(x)

        # 2. Categorical Inputs
        for name in self.categorical_cols:
            inputs[name] = keras.Input(shape=(1,), name=name, dtype='string')
            lookup = layers.StringLookup(
                vocabulary=self.vocabs[name],
                output_mode='one_hot',
                name=f'lookup_{name}'
            )
            x = lookup(inputs[name])
            all_features.append(x)

        # Combine
        x = layers.Concatenate()(all_features)

        # --- Hidden Layers ---
        for i in range(hp.Int('num_layers', 1, 3)):
            x = layers.Dense(
                units=hp.Int(f'units_{i}', 32, 256, step=32),
                activation='relu'
            )(x)
            if hp.Boolean('dropout'):
                x = layers.Dropout(hp.Float('dropout_rate', 0.1, 0.5))(x)
            x = layers.BatchNormalization()(x)

        # --- Output ---
        outputs = layers.Dense(1, activation='sigmoid')(x)
        model = keras.Model(inputs=inputs, outputs=outputs)

        model.compile(
            optimizer=keras.optimizers.Adam(hp.Choice('learning_rate', [1e-2, 1e-3, 1e-4])),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        return model


# ---------------------------------------------------
# 4. EXECUTION LOOP
# ---------------------------------------------------
if __name__ == "__main__":
    logger.info(f"Loading {DATA_PATH}...")
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        logger.error("train.csv not found!")
        sys.exit(1)

    # 1. Normalize Column Names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    target_clean = RAW_TARGET.lower().replace(' ', '_')

    # 2. Drop ID
    if 'id' in df.columns:
        df = df.drop(columns=['id'])

    # --- ROBUST TARGET CLEANING (THE FIX) ---
    logger.info(f"Original Target Values: {df[target_clean].unique()}")

    # Force to String, Lowercase, and Strip Whitespace
    # This ensures 'Presence ', 'Presence', and 'presence' are all treated as 'presence'
    df[target_clean] = df[target_clean].astype(str).str.strip().str.lower()

    # Define mapping for lowercase values
    mapping = {
        'presence': 1,
        'absence': 0,
        'yes': 1,
        'no': 0,
        '1': 1,
        '0': 0,
        'true': 1,
        'false': 0,
        '1.0': 1,
        '0.0': 0
    }

    logger.info("Applying mapping to target column...")
    df[target_clean] = df[target_clean].map(mapping)

    # CHECK FOR FAILURE
    if df[target_clean].isnull().any():
        logger.error("CRITICAL ERROR: Mapping failed for some values!")
        # Show exactly which rows failed
        failed_rows = df[df[target_clean].isnull()]
        logger.error(f"These values could not be mapped to 0 or 1: {failed_rows.index.tolist()}")
        logger.error("Please check your CSV file for unexpected values in the 'Heart Disease' column.")
        sys.exit(1)

    # Convert to Integers safely
    df[target_clean] = df[target_clean].astype(int)
    logger.info(f"Target successfully converted. Unique values: {df[target_clean].unique()}")

    # 3. Auto-Detect Features
    feature_df = df.drop(columns=[target_clean])
    numeric_cols = feature_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = feature_df.select_dtypes(include=['object', 'category']).columns.tolist()

    # 4. Split & Convert
    train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)
    train_ds = df_to_dataset(train_df, target_clean)
    val_ds = df_to_dataset(val_df, target_clean, shuffle=False)

    # 5. Initialize & Tune
    hypermodel = HeartDiseaseHyperModel(train_df, numeric_cols, categorical_cols)

    tuner = kt.Hyperband(
        hypermodel,
        objective='val_accuracy',
        max_epochs=20,
        factor=3,
        directory='my_nn_dir',
        project_name='heart_disease_kt_robust',  # New project name
        overwrite=True
    )

    logger.info("Starting Hyperparameter Search...")
    tuner.search(train_ds, validation_data=val_ds, epochs=20, callbacks=[keras.callbacks.EarlyStopping(patience=3)])

    # 6. Save Best Model
    best_model = tuner.get_best_models(num_models=1)[0]
    loss, accuracy = best_model.evaluate(val_ds)
    logger.info(f"Best Model Validation Accuracy: {accuracy:.2%}")

    save_path = ARTIFACT_DIR / "best_nn_model.keras"
    best_model.save(save_path)
    logger.info(f"Model saved to {save_path}")