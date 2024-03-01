from re import S
import pandas as pd
import matplotlib.pyplot as plt
from predict import predict
from scrape import scrape_comments
from analyze import collect_emotions

def collect_data(file1_name, file2_name, link1, link2):
    # scrape two yotutube videos
    scrape_comments(link1, 300, file1_name)
    scrape_comments(link2, 300, file2_name)

def store_data(file1_name, file2_name):
    # collect emotions from the comments
    sentiment_counts1 = collect_emotions(file1_name)
    sentiment_counts2 = collect_emotions(file2_name)

    #store the emotions in a csv file
    sentiment_df = pd.DataFrame([sentiment_counts1, sentiment_counts2], columns=["postive", "neutral", "negative"])
    sentiment_df.to_csv('data/emotions.csv', index=False)

def call_data(file_name):
    # load the data from the csv file
    df = pd.read_csv(file_name)
    # create two bar charts comparing the two videos
    fig, ax = plt.subplots(1, 2)

    # 
    ax[0].bar(['Positive', 'Neutral', 'Negative'], df.iloc[0], color=['blue', 'green', 'red'])
    ax[0].set_title('Coding Tutorial')
    ax[1].bar(['Positive', 'Neutral', 'Negative'], df.iloc[1], color=['blue', 'green', 'red'])
    ax[1].set_title('News Report')
    ax[0].set_ylim(0, 70)  # scale the y-axis to be the same for both charts
    ax[1].set_ylim(0, 70)

    # scale the y-axis to be the same for both charts
    plt.show()


file1_name = 'data/comments1.csv'
file2_name = 'data/comments2.csv'
link1 = 'tIeHLnjs5U8'
link2 = 'tgKdF8vwUco'

#collect_data(file1_name, file2_name, link1, link2)
#store_data(file1_name, file2_name)
call_data('data/emotions.csv')









