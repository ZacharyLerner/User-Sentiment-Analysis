from numpy import negative
import pandas as pd
import matplotlib.pyplot as plt
from predict import predict

def collect_emotions(file_name):
    # load the comments from the csv file
    df = pd.read_csv(file_name, on_bad_lines='skip')

    predictions = []
    
    # go through each comment and predict sentiment

    positive_sentiment = 0
    neutral_sentiment = 0
    negative_sentiment = 0

    sentiment_count = []

    for comment in df['text']:
        prediction = predict(comment)
        if prediction == 'Positive':
            positive_sentiment +=1 # positive sentiment
        elif prediction == 'Negative':
            negative_sentiment +=1  # negative sentiment
        else:
            neutral_sentiment +=1  # neutral sentiment

    sentiment_count.append(positive_sentiment)
    sentiment_count.append(negative_sentiment)
    sentiment_count.append(neutral_sentiment)

    return sentiment_count