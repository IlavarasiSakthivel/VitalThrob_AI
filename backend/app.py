from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import logging
import os
import traceback

# ---------------------------------------------------
# 1. SETUP & LOAD MODEL
# ---------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FlaskBackend")

# Get the base directory of your project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the Keras model
MODEL_PATH = os.path.join(BASE_DIR, "..", "artifacts_nn", "best_nn_model.keras")

logger.info(f"Loading TensorFlow Keras model from {MODEL_PATH}...")

try:
    model = tf.keras.models.load_model(MODEL_PATH)
    logger.info("Keras model loaded successfully.")
except Exception as e:
    logger.error(f"CRITICAL: Could not load Keras model: {e}")
    exit(1)

app = Flask(__name__)
CORS(app)

# ---------------------------------------------------
# 2. COLUMN MAPPING
# ---------------------------------------------------
# Expected feature order - this MUST match your training data
EXPECTED_FEATURES_ORDER = [
    'age', 'sex', 'chest_pain_type', 'bp', 'cholesterol',
    'fbs_over_120', 'ekg_results', 'max_hr', 'exercise_angina',
    'st_depression', 'slope_of_st', 'number_of_vessels_fluro', 'thallium'
]

# Frontend to backend mapping
FRONTEND_TO_BACKEND = {
    'Age': 'age',
    'Sex': 'sex',
    'Chest pain type': 'chest_pain_type',
    'BP': 'bp',
    'Cholesterol': 'cholesterol',
    'FBS over 120': 'fbs_over_120',
    'EKG results': 'ekg_results',
    'Max HR': 'max_hr',
    'Exercise angina': 'exercise_angina',
    'ST depression': 'st_depression',
    'Slope of ST': 'slope_of_st',
    'Number of vessels fluro': 'number_of_vessels_fluro',
    'Thallium': 'thallium'
}


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Heart Disease Neural Network API is Running!',
        'status': 'Active',
        'model_loaded': True,
        'expected_features': EXPECTED_FEATURES_ORDER,
        'usage': 'Send a POST request to /predict with patient data.'
    })


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        logger.info(f"Received prediction request with data: {data}")

        # 1. Map frontend names to backend names and convert values
        backend_data = {}
        for frontend_key, value in data.items():
            if frontend_key in FRONTEND_TO_BACKEND:
                backend_key = FRONTEND_TO_BACKEND[frontend_key]

                # Convert to float
                try:
                    backend_data[backend_key] = float(value)
                except ValueError:
                    # Handle string values
                    if value.lower() in ['yes', 'y', 'true', '1']:
                        backend_data[backend_key] = 1.0
                    elif value.lower() in ['no', 'n', 'false', '0']:
                        backend_data[backend_key] = 0.0
                    elif value.lower() in ['male', 'm']:
                        backend_data[backend_key] = 1.0
                    elif value.lower() in ['female', 'f']:
                        backend_data[backend_key] = 0.0
                    else:
                        # Try to convert to float
                        try:
                            backend_data[backend_key] = float(value)
                        except:
                            backend_data[backend_key] = 0.0

        logger.info(f"Mapped data: {backend_data}")

        # 2. Prepare feature dictionary for the model (13 separate inputs)
        model_inputs = {}
        missing_features = []

        for feature in EXPECTED_FEATURES_ORDER:
            if feature in backend_data:
                model_inputs[feature] = np.array([[backend_data[feature]]], dtype=np.float32)
            else:
                missing_features.append(feature)
                model_inputs[feature] = np.array([[0.0]], dtype=np.float32)

        if missing_features:
            logger.warning(f"Missing features: {missing_features}")

        logger.info(f"Model inputs prepared with shapes:")
        for key, value in model_inputs.items():
            logger.info(f"  {key}: {value.shape} = {value[0][0]}")

        # 3. Make prediction
        prediction = model.predict(model_inputs, verbose=0)
        logger.info(f"Raw model output: {prediction}")

        # Handle output (single value for binary classification)
        prediction_prob = float(prediction[0][0])

        # Ensure probability is between 0 and 1 (sigmoid output should already be)
        prediction_prob = max(0.0, min(1.0, prediction_prob))

        prediction_class = int(prediction_prob > 0.5)
        probability_pct = round(float(prediction_prob) * 100, 2)

        logger.info(f"Final prediction: class={prediction_class}, probability={probability_pct}%")

        return jsonify({
            'prediction': prediction_class,
            'probability': probability_pct,
            'features_used': EXPECTED_FEATURES_ORDER,
            'features_values': [float(model_inputs[f][0][0]) for f in EXPECTED_FEATURES_ORDER]
        })

    except Exception as e:
        logger.error(f"Prediction Error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


@app.route('/debug', methods=['GET'])
def debug():
    """Debug endpoint to test the model directly"""
    # Create test inputs as separate arrays
    test_inputs = {
        'age': np.array([[65.0]], dtype=np.float32),
        'sex': np.array([[1.0]], dtype=np.float32),
        'chest_pain_type': np.array([[4.0]], dtype=np.float32),
        'bp': np.array([[180.0]], dtype=np.float32),
        'cholesterol': np.array([[300.0]], dtype=np.float32),
        'fbs_over_120': np.array([[1.0]], dtype=np.float32),
        'ekg_results': np.array([[2.0]], dtype=np.float32),
        'max_hr': np.array([[120.0]], dtype=np.float32),
        'exercise_angina': np.array([[1.0]], dtype=np.float32),
        'st_depression': np.array([[4.5]], dtype=np.float32),
        'slope_of_st': np.array([[3.0]], dtype=np.float32),
        'number_of_vessels_fluro': np.array([[3.0]], dtype=np.float32),
        'thallium': np.array([[7.0]], dtype=np.float32)
    }

    try:
        prediction = model.predict(test_inputs, verbose=0)
        logger.info(f"Debug test prediction output: {prediction}")

        prediction_prob = float(prediction[0][0])
        prediction_class = int(prediction_prob > 0.5)

        return jsonify({
            'test_input': {k: v[0][0] for k, v in test_inputs.items()},
            'raw_prediction': prediction.tolist(),
            'prediction_class': prediction_class,
            'prediction_probability': float(prediction_prob),
            'probability_percent': round(float(prediction_prob) * 100, 2),
            'message': 'Debug test completed'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


@app.route('/test-low-risk', methods=['GET'])
def test_low_risk():
    """Test endpoint for low-risk values"""
    test_inputs = {
        'age': np.array([[40.0]], dtype=np.float32),
        'sex': np.array([[0.0]], dtype=np.float32),
        'chest_pain_type': np.array([[1.0]], dtype=np.float32),
        'bp': np.array([[120.0]], dtype=np.float32),
        'cholesterol': np.array([[180.0]], dtype=np.float32),
        'fbs_over_120': np.array([[0.0]], dtype=np.float32),
        'ekg_results': np.array([[0.0]], dtype=np.float32),
        'max_hr': np.array([[160.0]], dtype=np.float32),
        'exercise_angina': np.array([[0.0]], dtype=np.float32),
        'st_depression': np.array([[0.5]], dtype=np.float32),
        'slope_of_st': np.array([[1.0]], dtype=np.float32),
        'number_of_vessels_fluro': np.array([[0.0]], dtype=np.float32),
        'thallium': np.array([[3.0]], dtype=np.float32)
    }

    try:
        prediction = model.predict(test_inputs, verbose=0)
        prediction_prob = float(prediction[0][0])
        prediction_class = int(prediction_prob > 0.5)

        return jsonify({
            'test_input': {k: v[0][0] for k, v in test_inputs.items()},
            'prediction_class': prediction_class,
            'prediction_probability': float(prediction_prob),
            'probability_percent': round(float(prediction_prob) * 100, 2),
            'message': 'Low-risk test completed'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Heart Disease Prediction API")
    print("Server starting on http://127.0.0.1:5000")
    print(f"Model path: {MODEL_PATH}")
    print("=" * 60)
    app.run(debug=True, port=5000)