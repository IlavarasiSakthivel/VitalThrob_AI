import pandas as pd
import tensorflow as tf
import logging
from pathlib import Path

# ---------------------------------------------------
# 1. SETUP
# ---------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("Inference")

MODEL_PATH = Path("../artifacts_nn/best_nn_model.keras")
TEST_DATA_PATH = "../dataset/test.csv"
SUBMISSION_FILE = "../dataset/submission.csv"


def make_predictions():
    # ---------------------------------------------------
    # 2. LOAD MODEL
    # ---------------------------------------------------
    if not MODEL_PATH.exists():
        logger.error(f"Model not found at {MODEL_PATH}. Run train_model.py first!")
        return

    logger.info(f"Loading model from {MODEL_PATH}...")
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return

    # ---------------------------------------------------
    # 3. LOAD & PREP DATA
    # ---------------------------------------------------
    logger.info(f"Loading test data from {TEST_DATA_PATH}...")
    try:
        df = pd.read_csv(TEST_DATA_PATH)
    except FileNotFoundError:
        logger.error(f"{TEST_DATA_PATH} not found.")
        return

    # A. Normalize Column Names (Crucial!)
    # The model expects "age", "sex" (lowercase), but CSV might have "Age", "Sex"
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    logger.info(f"Columns normalized: {df.columns.tolist()}")

    # B. Handle ID
    if 'id' not in df.columns:
        logger.error("Test CSV is missing 'id' column.")
        return

    patient_ids = df.pop('id')  # Save IDs and remove from input

    # C. Convert to TensorFlow Friendly Format (Dictionary)
    # The model expects {'age': [...], 'sex': [...]}, not a DataFrame
    input_dict = {
        name: tf.convert_to_tensor(value)
        for name, value in df.items()
    }

    # ---------------------------------------------------
    # 4. PREDICT
    # ---------------------------------------------------
    logger.info("Running predictions...")

    # Predict returns probabilities (e.g., 0.85, 0.12)
    probs = model.predict(input_dict)

    # Convert probabilities to Class (0 or 1)
    # Threshold is 0.5 (Standard)
    predictions = (probs > 0.5).astype(int).flatten()

    # ---------------------------------------------------
    # 5. CREATE SUBMISSION
    # ---------------------------------------------------
    submission = pd.DataFrame({
        'id': patient_ids,
        'Heart Disease': predictions
    })

    # OPTIONAL: If the competition requires text (Presence/Absence) instead of 1/0
    # Uncomment the lines below if your submission gets rejected
    # mapping = {1: 'Presence', 0: 'Absence'}
    # submission['Heart Disease'] = submission['Heart Disease'].map(mapping)

    submission.to_csv(SUBMISSION_FILE, index=False)
    logger.info(f"✅ Success! Predictions saved to '{SUBMISSION_FILE}'")

    print("\n--- Preview ---")
    print(submission.head())


if __name__ == "__main__":
    make_predictions()

