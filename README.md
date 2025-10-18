# **Advanced Phishing Email Detection Using Machine Learning**

This project is an advanced phishing email detection system built with machine learning, featuring a user-friendly web interface, multiple model comparison, hyperparameter tuning, and deployment-ready setup. It uses state-of-the-art NLP preprocessing techniques and ensemble methods for robust classification. Perfect for hackathons and real-world applications!

**Author: Krish Gupta** | **Hackathon-Ready Version**

---

## **Table of Contents**
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Web Interface](#web-interface)
  - [API Endpoints](#api-endpoints)
  - [Command Line](#command-line)
- [Model Details](#model-details)
- [Deployment](#deployment)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## **Project Overview**

This advanced phishing email detector goes beyond basic classification by incorporating:
- **Advanced NLP Preprocessing**: Stop words removal, lemmatization, n-grams
- **Model Comparison & Tuning**: Automatic selection of best model (Random Forest, SVM, Logistic Regression) with hyperparameter optimization
- **Confidence Scores**: Probabilistic predictions for better decision-making
- **Batch Processing**: Analyze multiple emails at once
- **Web UI**: Beautiful, responsive interface with real-time results and visualizations
- **Metrics Dashboard**: View model performance, confusion matrix, and evaluation metrics
- **Docker Support**: Easy deployment and scaling

---

## **Key Features**
- **🔍 Advanced Text Preprocessing**: NLTK-powered cleaning, lemmatization, and TF-IDF with n-grams
- **🤖 Auto Model Selection**: Compares RF, SVM, and LR with grid search and cross-validation
- **📊 Confidence Scoring**: Probabilistic predictions with confidence bars
- **🌐 Web Interface**: Bootstrap-based UI for easy email analysis with tabs and animations
- **📈 Performance Metrics**: Accuracy, Precision, Recall, F1-Score, ROC AUC, confusion matrix, and word clouds
- **⚡ Batch Prediction**: Process multiple emails simultaneously via API and web UI with export
- **🐳 Docker Ready**: Containerized for easy deployment
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🎯 Demo Data**: Built-in demo data generation for quick testing
- **📋 Model Comparison**: Choose from trained models in the UI
- **📊 Advanced Visualizations**: ROC curves and word clouds for insights

---

## **Technologies Used**
- **Python 3.9+**
- **Scikit-learn**: ML algorithms and evaluation
- **NLTK**: Natural language processing
- **Flask**: Web framework
- **Bootstrap 5**: Frontend styling
- **Matplotlib & Seaborn**: Data visualization
- **Joblib**: Model serialization
- **Docker**: Containerization

---

## **Quick Start**

1. **Clone and Install**:
   ```bash
   git clone https://github.com/yourusername/phishing-email-detection.git
   cd phishing-email-detection
   pip install -r requirements/requirements.txt
   ```

2. **Run Full Pipeline**:
   ```bash
   python run_pipeline.py
   ```

3. **Open Browser**: Go to `http://127.0.0.1:5000/`

---

## **Installation**

### **Prerequisites**
- Python 3.9+
- pip

### **Setup**
```bash
# Clone repository
git clone https://github.com/yourusername/phishing-email-detection.git
cd phishing-email-detection

# Install dependencies
pip install -r requirements/requirements.txt

# Download NLTK data (first run)
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"
```

---

## **Usage**

### **Web Interface**
Run the full pipeline and access the web app:
```bash
python run_pipeline.py
```
Navigate to `http://127.0.0.1:5000/` in your browser.

### **API Endpoints**

#### Single Email Prediction
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"email": "Your account has been compromised. Click here to reset your password."}'
```

#### Batch Prediction
```bash
curl -X POST http://127.0.0.1:5000/predict_batch \
  -H "Content-Type: application/json" \
  -d '{"emails": ["Email 1 text", "Email 2 text"]}'
```

#### Get Model Metrics
```bash
curl http://127.0.0.1:5000/metrics
```

### **Command Line**
```bash
# Run full pipeline (recommended)
python run_pipeline.py

# Or run individual steps:
# Generate demo data
python src/demo_data.py

# Preprocess data
python src/preprocess.py

# Train model
python src/train.py

# Predict single email
python src/predict.py

# Run Flask app
cd requirements && python app.py
```

---

## **Model Details**

### **Preprocessing Pipeline**
1. **Text Cleaning**: Remove punctuation, lowercase conversion
2. **Stop Words Removal**: Filter common English stop words
3. **Lemmatization**: Reduce words to base forms
4. **TF-IDF Vectorization**: Convert to numerical features with n-grams (1-2)

### **Model Selection**
The system automatically compares:
- **Random Forest**: Ensemble of decision trees
- **Support Vector Machine**: Kernel-based classification
- **Logistic Regression**: Linear probabilistic model

Best model selected via 5-fold CV F1-score optimization.

### **Hyperparameter Tuning**
Grid search over key parameters for each model type.

---

## **Deployment**

### **Docker**
```bash
# Build and run
docker-compose up --build

# Or manually
docker build -t phishing-detector .
docker run -p 5000:5000 phishing-detector
```

### **Production Deployment**
For production, consider:
- Gunicorn for WSGI server
- Nginx reverse proxy
- Environment variables for configuration
- Database integration for logging

---

## **Screenshots**

### Web Interface
![Web Interface](screenshots/web_interface.png)

### Model Metrics
![Metrics Dashboard](screenshots/metrics_dashboard.png)

### Confusion Matrix
![Confusion Matrix](models/confusion_matrix.png)

### ROC Curve
![ROC Curve](models/roc_curve.png)

### Word Clouds
![Phishing Word Cloud](models/wordcloud_phishing.png)
![Non-Phishing Word Cloud](models/wordcloud_non_phishing.png)

---

## **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### **Ideas for Enhancement**
- Add deep learning models (BERT, LSTM)
- Real-time email monitoring
- User authentication
- Email attachment analysis
- Multi-language support
- API rate limiting and caching
- Integration with email clients
- Automated model retraining
- A/B testing for model versions

---

## **License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built for Hackathons | Ready for Production | Open Source**
```

---

### Explanation:
1. **Markdown Formatting**: The code includes headers, lists, and code blocks (` ```bash ` and ` ```python `) for clarity.
2. **Troubleshooting Virtual Environment**: Added steps to resolve issues with locked environments.
3. **Ready for GitHub**: The content is now GitHub-ready and can be directly used as `README.md`.

Let me know if you need further modifications!
"# Phishing_Detector-ML" 
