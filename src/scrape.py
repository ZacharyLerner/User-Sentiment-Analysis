# credit to Adam from the GitHub repository "analyticswithadam/Python"
'''
The following code was adapted from the notebook "YouTube_Comments_Advanced.ipynb" 
by Adam from the GitHub repository "analyticswithadam/Python" (https://github.com/analyticswithadam/Python). 
'''

import googleapiclient.discovery
import pandas as pd
import numpy as np
import re

def clean_comments(df):
    # clean the data for special characters and new lines
    df['text'] = df['text'].replace('\n',' ', regex=True)
    df['text'] = df['text'].str.lower()
    df['text'] = df['text'].str.strip()
    # Replace empty strings with np.nan
    df.replace('', np.nan)
    # Now use dropna()
    df = df.dropna()
    # drop duplicate authors
    df = df.drop_duplicates(subset='author', keep='last')

    # save the data to a csv file based on the inputed file name
    return df

def scrape_comments(video_id, max_results, file_name):
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = #key

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results
    )

    comments = []

    # Execute the request.
    response = request.execute()

    # Get the comments from the response.
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        public = item['snippet']['isPublic']
        if (int(comment['likeCount']) > 1) and (len(comment['textOriginal']) > 10):
            comments.append([
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['likeCount'],
                comment['textOriginal'],
                public
            ])

    while len(comments) < max_results:
        try:
            nextPageToken = response['nextPageToken']
        except KeyError:
            break
        # Create a new request object with the next page token.
        nextRequest = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            pageToken=nextPageToken
        )
        # Execute the next request.
        response = nextRequest.execute()
        # Get the comments from the next response.
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            public = item['snippet']['isPublic']
            if (int(comment['likeCount']) > 1) and (len(comment['textOriginal']) > 10):
                comments.append([
                    comment['authorDisplayName'],
                    comment['publishedAt'],
                    comment['likeCount'],
                    comment['textOriginal'],
                    public
                ])
            # Break the loop if we have enough comments.
            if len(comments) >= max_results:
                break

    df = pd.DataFrame(comments, columns=['author', 'updated_at', 'like_count', 'text','public'])

    # clean the data for special characters and new lines
    df = clean_comments(df)

    # save the data to a csv file based on the inputed file name
    df.to_csv(file_name, index=False)

scrape_comments('AF8d72mA41M', 500, 'data/comments3.csv')
