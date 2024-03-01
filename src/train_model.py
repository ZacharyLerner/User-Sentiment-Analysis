# train_model.py

# Importing required libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
from joblib import dump


# Load dataset from file
def load_data(file_path):
    data = pd.read_csv(file_path)
    data = data.dropna()
    data = data.drop_duplicates()
    return data

# Convert text data into numerical features using TF-IDF
def vectorize_text(X_train, X_test):
    # creates a TF-IDF vectorizer object with 10000 features
    tfidf_vectorizer = TfidfVectorizer(max_features=10000)
    # Learn vocabulary and idf from training set
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    # Transform documents to document-term matrix.
    X_test_tfidf = tfidf_vectorizer.transform(X_test)

    return X_train_tfidf, X_test_tfidf, tfidf_vectorizer
# Train the SVM model
def train_svm_model(X_train_tfidf, y_train):
    # creates an instance of a learning model
    svm_model = SVC(kernel='linear')
    # fit the model to the training data
    svm_model.fit(X_train_tfidf, y_train)

    return svm_model

# evaluates the trained model
def evaluate_model(model, X_test_tfidf, y_test):
    # predict the labels based on the current data set
    y_pred = model.predict(X_test_tfidf)
    # calculate the accuracy of the model
    accuracy = accuracy_score(y_test, y_pred)


    return accuracy

# Save the trained model to disk
def save_model(model, file_path):
    # saved to file path
    dump(model, file_path)

# Main function
def main():
    # data loaded from csv file
    data = load_data('data/twitter_training.csv')

    # splits the dataset into two axis
    x = data['text']
    y = data['sentiment']

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Convert text data into numerical features using TF-IDF
    X_train_tfidf, X_test_tfidf, tfidf_vectorizer = vectorize_text(X_train, X_test)

    # Train the SVM model
    svm_model = train_svm_model(X_train_tfidf, y_train)

    # Evaluate the model
    accuracy= evaluate_model(svm_model, X_test_tfidf, y_test)

    # Print the results
    print("Accuracy:", accuracy)
    # Save model
    save_model(tfidf_vectorizer, "models/vectorizer.joblib")
    save_model(svm_model, "models/svm_model.joblib")

main()