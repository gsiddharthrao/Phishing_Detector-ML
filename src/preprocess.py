import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

def parse_email_headers(email_text):
    """Parse email headers and return a dict of extracted features."""
    headers = {}
    lines = email_text.split('\n')
    current_header = None
    for line in lines:
        if ':' in line and not line.startswith(' '):
            key, value = line.split(':', 1)
            current_header = key.strip().lower()
            headers[current_header] = value.strip()
        elif current_header and line.startswith(' '):
            headers[current_header] += ' ' + line.strip()
    return headers

def extract_header_features(headers):
    """Extract useful features from headers."""
    features = []
    # Sender domain
    from_header = headers.get('from', '')
    sender_domain = ''
    match = re.search(r'@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', from_header)
    if match:
        sender_domain = match.group(1).lower()
    features.append(f"sender_domain:{sender_domain}")

    # Subject keywords
    subject = headers.get('subject', '').lower()
    urgency_words = ['urgent', 'alert', 'security', 'verify', 'account', 'password', 'reset', 'suspended']
    for word in urgency_words:
        if word in subject:
            features.append(f"subject_{word}:1")
    features.append(f"subject_length:{len(subject)}")

    # To domain
    to_header = headers.get('to', '')
    to_domain = ''
    match = re.search(r'@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', to_header)
    if match:
        to_domain = match.group(1).lower()
    features.append(f"to_domain:{to_domain}")

    return ' '.join(features)

def preprocess_data(input_file, output_file):
    # Download NLTK data if not present
    nltk.download('stopwords')
    nltk.download('wordnet')

    # Load the CSV file
    data = pd.read_csv(input_file)

    # Ensure the dataset has 'text' and 'label' columns
    if 'text' not in data.columns or 'label' not in data.columns:
        raise ValueError("Input CSV must have 'text' and 'label' columns.")

    # Preprocess text
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    def clean_text(text):
        # Parse headers
        headers = parse_email_headers(text)
        header_features = extract_header_features(headers)

        # Remove headers from body (simple way: assume headers end before body)
        # For simplicity, if 'from:' is present, treat as full email
        body_start = text.find('\n\n')  # Common separator
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

    data['cleaned_text'] = data['text'].apply(clean_text)

    # Vectorize the text using TF-IDF with n-grams
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
    X = vectorizer.fit_transform(data['cleaned_text']).toarray()

    # Extract labels
    y = data['label'].values

    # Save preprocessed data and vectorizer
    with open(output_file, "wb") as f:
        pickle.dump((X, y, vectorizer), f)

    print(f"Preprocessed data saved to {output_file}")

if __name__ == "__main__":
    # Try demo data first, fall back to original if not available
    import os
    if os.path.exists("data/demo_phishing_emails.csv"):
        preprocess_data("data/demo_phishing_emails.csv", "data/preprocessed_data.pkl")
    else:
        preprocess_data("data/phishing_emails.csv", "data/preprocessed_data.pkl")
