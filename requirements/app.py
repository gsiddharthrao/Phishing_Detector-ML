from flask import Flask, request, jsonify, render_template, send_from_directory, Blueprint, current_app
import sys
import os
import sys
import os

# Add project root to path to allow importing 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.predict import predict_email, predict_batch
import pickle
import logging
from flask_cors import CORS

class Config:
    """Flask configuration variables."""
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')
    DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
    MODEL_FILE = os.path.join(MODELS_DIR, 'phishing_detector.pkl')
    PREPROCESSED_DATA_FILE = os.path.join(DATA_DIR, 'preprocessed_data.pkl')
    METRICS_FILE = os.path.join(MODELS_DIR, 'metrics.pkl')


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use a Blueprint for better organization
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/predict', methods=['POST'])
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
        result, confidence, url_report, explanation = predict_email(
            current_app.config['MODEL_FILE'],
            current_app.config['PREPROCESSED_DATA_FILE'],
            email, model_name
        )
        logger.info(f"Prediction result: {result}, confidence: {confidence}")
        return jsonify({
            "prediction": result,
            "confidence": confidence,
            "link_report": url_report,
            "explanation": explanation
        })
    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@main_bp.route('/predict_batch', methods=['POST'])
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
        results = predict_batch(
            current_app.config['MODEL_FILE'],
            current_app.config['PREPROCESSED_DATA_FILE'],
            emails, model_name
        )
        logger.info(f"Batch prediction completed for {len(results)} emails")
        return jsonify({
            "results": [
                {"prediction": r[0], "confidence": r[1], "link_report": r[2], "explanation": r[3]} for r in results
            ]
        })
    except Exception as e:
        logger.error(f"Error in predict_batch endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@main_bp.route('/metrics')
def metrics():
    try:
        with open(current_app.config['METRICS_FILE'], 'rb') as f:
            metrics = pickle.load(f)
        logger.info("Metrics retrieved successfully")
        return jsonify(metrics)
    except FileNotFoundError:
        logger.error("Metrics file not found")
        return jsonify({"error": "Metrics not available"}), 404
    except Exception as e:
        logger.error(f"Error retrieving metrics: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

def serve_image(filename, error_message):
    """Helper function to serve an image from the models directory."""
    try:
        return send_from_directory(current_app.config['MODELS_DIR'], filename)
    except Exception as e:
        logger.error(f"Error serving {filename}: {str(e)}")
        return jsonify({"error": error_message}), 404

@main_bp.route('/confusion_matrix')
def confusion_matrix(): return serve_image('confusion_matrix.png', "Confusion matrix not available")
@main_bp.route('/wordcloud_phishing')
def wordcloud_phishing(): return serve_image('wordcloud_phishing.png', "Wordcloud not available")
@main_bp.route('/wordcloud_non_phishing')
def wordcloud_non_phishing(): return serve_image('wordcloud_non_phishing.png', "Wordcloud not available")
@main_bp.route('/roc_curve')
def roc_curve(): return serve_image('roc_curve.png', "ROC curve not available")

@main_bp.route('/models_list')
def models_list():
    try:
        # Dynamically get model names from the metrics file
        with open(current_app.config['METRICS_FILE'], 'rb') as f:
            metrics = pickle.load(f)
        # The keys of the metrics dictionary are the model names
        model_names = list(metrics.keys())
        return jsonify({"models": model_names})
    except Exception as e:
        logger.error(f"Error retrieving models list: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

def create_app(config_class=Config):
    # Adjust path to find src module
    sys.path.append(config_class.PROJECT_ROOT)

    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app)

    app.register_blueprint(main_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
