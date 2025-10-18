import joblib
import json
import os
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

def convert_model_to_onnx(model_data_path, output_dir):
    """
    Converts the trained scikit-learn classifier to ONNX format and
    saves the vectorizer's vocabulary to a JSON file.
    """
    print("Loading model and vectorizer...")
    # The .pkl file contains a dictionary with the model and vectorizer
    model_data = joblib.load(model_data_path)
    
    # Extract the best model and the vectorizer
    # Ensure these keys match what's saved in your train.py
    model = model_data.get('best_model')
    vectorizer = model_data.get('vectorizer')

    if model is None or vectorizer is None:
        print("Error: 'best_model' or 'vectorizer' not found in the model file.")
        return

    # --- 1. Save the Vectorizer's Vocabulary ---
    print("Saving vectorizer vocabulary...")
    vocabulary = vectorizer.get_feature_names_out()
    vocab_path = os.path.join(output_dir, 'vocabulary.json')
    os.makedirs(output_dir, exist_ok=True)
    with open(vocab_path, 'w') as f:
        json.dump(vocabulary.tolist(), f)
    print(f"Vocabulary saved to {vocab_path}")

    # --- 2. Convert the Classifier to ONNX ---
    # The number of features is the size of the TF-IDF vocabulary
    n_features = len(vocabulary)
    print(f"Model has {n_features} input features.")

    print("Converting model to ONNX...")
    # The input type for the ONNX model.
    # [None, n_features] means the model accepts a batch of any size,
    # where each input has n_features.
    initial_type = [('float_input', FloatTensorType([None, n_features]))]

    onx = convert_sklearn(model, initial_types=initial_type)

    onnx_model_path = os.path.join(output_dir, 'model.onnx')
    with open(onnx_model_path, "wb") as f:
        f.write(onx.SerializeToString())
    print(f"Model converted and saved to {onnx_model_path}")

if __name__ == "__main__":
    convert_model_to_onnx(
        "models/phishing_detector.pkl",
        "browser_extension/js"
    )
