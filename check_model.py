import pickle
import json
import os

print("Checking model files...")

# Try to load the large model
try:
    with open('artifacts/heart_disease_model.pkl', 'rb') as f:
        model = pickle.load(f)
        print(f"Successfully loaded heart_disease_model.pkl")
        print(f"Model type: {type(model)}")
        if hasattr(model, '__class__'):
            print(f"Model class: {model.__class__.__name__}")
except Exception as e:
    print(f"Failed to load heart_disease_model.pkl: {e}")

print("\n" + "="*50 + "\n")

# Try to load the smaller model
try:
    with open('artifacts/model.pkl', 'rb') as f:
        model2 = pickle.load(f)
        print(f"Successfully loaded model.pkl")
        print(f"Model type: {type(model2)}")
        if hasattr(model2, '__class__'):
            print(f"Model class: {model2.__class__.__name__}")
except Exception as e:
    print(f"Failed to load model.pkl: {e}")

print("\n" + "="*50 + "\n")

# Also check the preprocessor
try:
    with open('preprocessor.pkl', 'rb') as f:
        preprocessor = pickle.load(f)
        print(f"Successfully loaded preprocessor.pkl")
        print(f"Preprocessor type: {type(preprocessor)}")
        if hasattr(preprocessor, '__class__'):
            print(f"Preprocessor class: {preprocessor.__class__.__name__}")
except Exception as e:
    print(f"Failed to load preprocessor.pkl: {e}")
