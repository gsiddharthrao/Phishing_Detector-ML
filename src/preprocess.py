import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

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
        text = re.sub(r'[^\w\s]', '', text.lower())  # Remove punctuation and lowercase
        words = text.split()
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
        return ' '.join(words)

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
