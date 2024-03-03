import pandas as pd
from predict import predict
import numpy as np
import matplotlib.pyplot as plt


def date_sentiment(file_name, time_unit):
    # load the comments from the csv file
    df = pd.read_csv(file_name, on_bad_lines='skip')
    # sort the comments by date
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    df = df.sort_values(by='updated_at')

    if time_unit == 'years':
        time_data = df['updated_at'].dt.year.unique()
    elif time_unit == 'months':
        time_data = df['updated_at'].dt.to_period('M').unique()
    elif time_unit == 'days':
        time_data = df['updated_at'].dt.date.unique()
    elif time_unit == 'hours':
        time_data = df['updated_at'].dt.to_period('H').unique()
    else:
        print("Invalid time unit. Please choose from 'years', 'months', 'days', or 'hours'.")
        return

    time_sentiment = []
    for time in time_data:
        time_sentiment.append([time, 0])

    for time in time_data:
        for index, row in df.iterrows():
            if time_unit == 'years' and time == row['updated_at'].year:
                sentiment = predict(row['text'])
                if sentiment == 'Positive':
                    time_sentiment[time_data.tolist().index(time)][1] += 1
                elif sentiment == 'Negative':
                    time_sentiment[time_data.tolist().index(time)][1] -= 1
            elif time_unit == 'months' and time == row['updated_at'].to_period('M'):
                sentiment = predict(row['text'])
                if sentiment == 'Positive':
                    time_sentiment[time_data.tolist().index(time)][1] += 1
                elif sentiment == 'Negative':
                    time_sentiment[time_data.tolist().index(time)][1] -= 1
            elif time_unit == 'days' and time == row['updated_at'].date():
                sentiment = predict(row['text'])
                if sentiment == 'Positive':
                    time_sentiment[time_data.tolist().index(time)][1] += 1
                elif sentiment == 'Negative':
                    time_sentiment[time_data.tolist().index(time)][1] -= 1
            elif time_unit == 'hours' and time == row['updated_at'].to_period('H'):
                sentiment = predict(row['text'])
                if sentiment == 'Positive':
                    time_sentiment[time_data.tolist().index(time)][1] += 1
                elif sentiment == 'Negative':
                    time_sentiment[time_data.tolist().index(time)][1] -= 1

    print(time_sentiment)

    # plot this as a line graph
    fig, ax = plt.subplots()
    ax.plot([str(time) for time in time_data], [sentiment[1] for sentiment in time_sentiment])
    ax.set_title('Sentiment over Time')

    # create a line of best fit for the data and plot it on the graph
    x = [time_data.tolist().index(time) for time in time_data]
    y = [sentiment[1] for sentiment in time_sentiment]
    m, b = np.polyfit(x, y, deg=1)
    plt.plot(x, [m * xi + b for xi in x])
    plt.show()


date_sentiment('data/comments3.csv', 'days')
