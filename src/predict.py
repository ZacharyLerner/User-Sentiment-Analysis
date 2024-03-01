# Import necessary libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import load
import re

# Load the trained model and vectorizer from file
model = load("models/svm_model.joblib")
vectorizer = load('models/vectorizer.joblib')

# Preprocess the input text data, currently just lowercase the text
def preprocess_text(text):
    text = str(text).lower()
    punctuation_pattern = r'[^\w\s]'  # Matches any character that is not a word character or whitespace
    # Use the sub() function from the re module to replace all matches of the pattern with an empty string
    processed_text = re.sub(punctuation_pattern, '', text)
    return processed_text

# Vectorize the preprocessed text data using the TF-IDF vectorizer
def vectorize_text(text):
    text_vectorized = vectorizer.transform([text])
    return text_vectorized

# Make predictions using the trained model
def make_predictions(text_vectorized):
    prediction = model.predict(text_vectorized)
    return prediction

def predict(input_text):
    # Preprocess the input text data
    preprocessed_text = preprocess_text(input_text)

    # Vectorize the preprocessed text data using the TF-IDF vectorizer
    text_vectorized = vectorize_text(preprocessed_text)

    # Make predictions using the trained model
    prediction = make_predictions(text_vectorized)

    return prediction[0]