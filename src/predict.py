import joblib
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def preprocess_single_email(email_text):
    # Download NLTK data if not present
    nltk.download('stopwords')
    nltk.download('wordnet')

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    def clean_text(text):
        text = re.sub(r'[^\w\s]', '', text.lower())  # Remove punctuation and lowercase
        words = text.split()
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
        return ' '.join(words)

    return clean_text(email_text)

def predict_email(model_file, vectorizer_file, email_text, model_name='best'):
    # Load the model
    if model_name == 'best':
        model = joblib.load(model_file)
    else:
        model = joblib.load(f'models/{model_name.lower()}_model.pkl')

    # Load the vectorizer
    with open(vectorizer_file, "rb") as f:
        _, _, vectorizer = pickle.load(f)

    # Preprocess the input email
    cleaned_email = preprocess_single_email(email_text)

    # Vectorize the input email
    email_vector = vectorizer.transform([cleaned_email]).toarray()

    # Make a prediction
    prediction = model.predict(email_vector)
    prediction_proba = model.predict_proba(email_vector)[0]

    result = "Phishing" if prediction[0] == 1 else "Not Phishing"
    confidence = prediction_proba[1] if prediction[0] == 1 else prediction_proba[0]

    return result, confidence

def predict_batch(model_file, vectorizer_file, emails, model_name='best'):
    # Load the model
    if model_name == 'best':
        model = joblib.load(model_file)
    else:
        model = joblib.load(f'models/{model_name.lower()}_model.pkl')

    # Load the vectorizer
    with open(vectorizer_file, "rb") as f:
        _, _, vectorizer = pickle.load(f)

    # Preprocess emails
    cleaned_emails = [preprocess_single_email(email) for email in emails]

    # Vectorize the input emails
    email_vectors = vectorizer.transform(cleaned_emails).toarray()

    # Make predictions
    predictions = model.predict(email_vectors)
    predictions_proba = model.predict_proba(email_vectors)

    results = []
    for i, pred in enumerate(predictions):
        result = "Phishing" if pred == 1 else "Not Phishing"
        confidence = predictions_proba[i][1] if pred == 1 else predictions_proba[i][0]
        results.append((result, confidence))

    return results

if __name__ == "__main__":
    email_text = "Your account has been compromised. Click here to reset your password."
    result, confidence = predict_email("models/phishing_detector.pkl", "data/preprocessed_data.pkl", email_text)
    print(f"Prediction: {result}, Confidence: {confidence:.2f}")
