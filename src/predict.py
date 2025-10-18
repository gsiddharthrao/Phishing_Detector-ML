import joblib
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from .url_scanner import analyze_urls_in_text
from .preprocess import parse_email_headers, extract_header_features

def preprocess_single_email(email_text):
    # Download NLTK data if not present
    try:
        stopwords.words('english')
    except LookupError:
        nltk.download('stopwords')
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    def clean_text(text):
        # Parse headers
        headers = parse_email_headers(text)
        header_features = extract_header_features(headers)

        # Remove headers from body
        body_start = text.find('\n\n')
        if body_start == -1:
            body = text
        else:
            body = text[body_start:].strip()

        # Clean body
        body = re.sub(r'[^\w\s]', '', body.lower())
        words = body.split()
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
        cleaned_body = ' '.join(words)

        # Combine header features with cleaned body
        return cleaned_body + ' ' + header_features

    return clean_text(email_text)

def extract_sender_domain(email_text):
    """Extracts the sender's domain from the 'From' line."""
    # First try the new header parsing
    headers = parse_email_headers(email_text)
    from_header = headers.get('from', '')
    match = re.search(r'@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', from_header)
    if match:
        return match.group(1).lower()
    # Fallback to old method
    match = re.search(r"From:.*?<(.+?)>", email_text, re.IGNORECASE)
    if match:
        sender_email = match.group(1).strip()
        if '@' in sender_email:
            return sender_email.split('@')[1].lower()
    return None

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

    # --- Sender and URL Verification Logic ---
    url_report = analyze_urls_in_text(email_text)
    sender_domain = extract_sender_domain(email_text)
    link_domains = {url['domain'] for url in url_report}

    domain_mismatch_warning = None
    if sender_domain and link_domains:
        # Check if at least one link domain is a subdomain of or matches the sender domain
        # e.g., sender is 'google.com', link is 'mail.google.com' -> OK
        if not any(link_domain.endswith(sender_domain) for link_domain in link_domains):
            # To reduce noise, only warn if the sender domain is not a generic free email provider
            generic_providers = {'gmail.com', 'yahoo.com', 'outlook.com', 'aol.com'}
            if sender_domain not in generic_providers:
                first_link_domain = next(iter(link_domains))
                domain_mismatch_warning = f"Warning: Email is from {sender_domain} but links go to a different domain ({first_link_domain})."

    # --- Explanation Generation ---
    explanation_parts = []
    if result == 'Phishing':
        explanation_parts.append('Model predicts phishing based on textual features and learned patterns')
    else:
        explanation_parts.append('Model predicts not phishing based on textual features')

    # Add sender verification warning if present
    if domain_mismatch_warning:
        explanation_parts.append(domain_mismatch_warning)

    # Add URL-based cues
    if url_report:
        suspicious = [u['summary'] for u in url_report if u.get('summary') and 'suspicious' in u.get('summary', '')]
        if suspicious:
            explanation_parts.append('Links found: ' + '; '.join(suspicious))
        elif not domain_mismatch_warning: # Avoid being redundant
            explanation_parts.append('Links found and appear benign by quick heuristics')

    explanation = '. '.join(explanation_parts) + '.'

    return result, confidence, url_report, explanation

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
        url_report = analyze_urls_in_text(emails[i])

        explanation_parts = []
        if result == 'Phishing':
            explanation_parts.append('Model predicts phishing based on textual features')
        else:
            explanation_parts.append('Model predicts not phishing based on textual features')
        if url_report:
            suspicious = [u['summary'] for u in url_report if u.get('summary') and 'suspicious' in u.get('summary', '')]
            if suspicious:
                explanation_parts.append('Links: ' + '; '.join(suspicious))
            else:
                explanation_parts.append('Links present and appear benign by quick heuristics')
        explanation = '. '.join(explanation_parts) + '.'

        results.append((result, confidence, url_report, explanation))

    return results

if __name__ == "__main__":
    email_text = "Your account has been compromised. Click here to reset your password."
    result, confidence = predict_email("models/phishing_detector.pkl", "data/preprocessed_data.pkl", email_text)
    print(f"Prediction: {result}, Confidence: {confidence:.2f}")
