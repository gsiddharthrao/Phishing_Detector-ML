from flask import Flask, request, jsonify, render_template, send_from_directory
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.predict import predict_email, predict_batch
import pickle
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({"error": "Invalid JSON data"}), 400

        email = data.get('email')
        model_name = data.get('model', 'best')  # Default to best model

        if not email:
            logger.error("Email text is required")
            return jsonify({"error": "Email text is required"}), 400

        logger.info(f"Predicting for email with model: {model_name}")
        result, confidence = predict_email("models/phishing_detector.pkl", "data/preprocessed_data.pkl", email, model_name)
        logger.info(f"Prediction result: {result}, confidence: {confidence}")
        return jsonify({"prediction": result, "confidence": confidence})
    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/predict_batch', methods=['POST'])
def predict_batch_endpoint():
    try:
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({"error": "Invalid JSON data"}), 400

        emails = data.get('emails')
        model_name = data.get('model', 'best')  # Default to best model

        if not emails or not isinstance(emails, list):
            logger.error("A list of emails is required")
            return jsonify({"error": "A list of emails is required"}), 400

        logger.info(f"Batch predicting {len(emails)} emails with model: {model_name}")
        results = predict_batch("models/phishing_detector.pkl", "data/preprocessed_data.pkl", emails, model_name)
        logger.info(f"Batch prediction completed for {len(results)} emails")
        return jsonify({"results": [{"prediction": r[0], "confidence": r[1]} for r in results]})
    except Exception as e:
        logger.error(f"Error in predict_batch endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/metrics')
def metrics():
    try:
        with open('models/metrics.pkl', 'rb') as f:
            metrics = pickle.load(f)
        logger.info("Metrics retrieved successfully")
        return jsonify(metrics)
    except FileNotFoundError:
        logger.error("Metrics file not found")
        return jsonify({"error": "Metrics not available"}), 404
    except Exception as e:
        logger.error(f"Error retrieving metrics: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/confusion_matrix')
def confusion_matrix():
    try:
        return send_from_directory('models', 'confusion_matrix.png')
    except Exception as e:
        logger.error(f"Error serving confusion matrix: {str(e)}")
        return jsonify({"error": "Confusion matrix not available"}), 404

@app.route('/wordcloud_phishing')
def wordcloud_phishing():
    try:
        return send_from_directory('models', 'wordcloud_phishing.png')
    except Exception as e:
        logger.error(f"Error serving phishing wordcloud: {str(e)}")
        return jsonify({"error": "Wordcloud not available"}), 404

@app.route('/wordcloud_non_phishing')
def wordcloud_non_phishing():
    try:
        return send_from_directory('models', 'wordcloud_non_phishing.png')
    except Exception as e:
        logger.error(f"Error serving non-phishing wordcloud: {str(e)}")
        return jsonify({"error": "Wordcloud not available"}), 404

@app.route('/roc_curve')
def roc_curve():
    try:
        return send_from_directory('models', 'roc_curve.png')
    except Exception as e:
        logger.error(f"Error serving ROC curve: {str(e)}")
        return jsonify({"error": "ROC curve not available"}), 404

@app.route('/models_list')
def models_list():
    try:
        models = ['RandomForest', 'LogisticRegression', 'SVM']
        return jsonify({"models": models})
    except Exception as e:
        logger.error(f"Error retrieving models list: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
