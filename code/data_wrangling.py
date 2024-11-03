import pandas as pd
import preprocessor as p
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *

import tweet_webscraping

MIN_YR = tweet_webscraping.MIN_YR
MAX_YR = tweet_webscraping.MAX_YR

# Returns a dataframe containing all the raw tweets
def getTweets():
    try:
        # Check if the file with all tweets exists
        tweets_df = pd.read_csv(f"data/tweets.csv", lineterminator='\n')

    except FileNotFoundError:
        # If there isn't a file with all tweets, make a file with all tweets
        # and save it
        tweets = []
        for year in range(MIN_YR, MAX_YR + 1):
            tweets.append(pd.read_csv(f"data/tweets_{year}.csv",
                                      lineterminator='\n', index_col = 0))

        tweets_df = pd.concat(tweets)
        tweets_df.to_csv("data/tweets.csv", header = True, index = False)

    return tweets_df

def cleanData(tweets_df):
    # Clean data by removing names, links, hashtags, and emojis
    tweets_df["clean_text"] = tweets_df["text"].map(lambda txt: p.clean(txt).lower())

    # Remove stop words
    allowed_words = ["no", "not", "can't", "shouldn't", "doesn't", "don't", "isn't"]
    stop = stopwords.words('english')
    #tweets_df['clean_text'] = tweets_df['clean_text'].apply(lambda x: ' '.join(
    #                            [word for word in x.split() if word not in (stop)
    #                             or word in (allowed_words)]))

    #Remove unneccessary columns
    tweets_df = tweets_df.drop(['year', 'month', 'text'], axis = 1)

    # Remove time from datetime
    tweets_df['datetime'] = tweets_df['datetime'].apply(lambda txt: txt.split()[0])
    tweets_df.rename(columns = {'datetime':'date'}, inplace = True)

    # Remove duplicate entries or missing entries from the clean_data column
    tweets_df = tweets_df.drop_duplicates(subset = ['clean_text', 'date'])
    tweets_df = tweets_df.dropna()

    return tweets_df

def applySentimentAnalysis(tweets_df):
    # Apply sentiment algorithm and add the polarity score to each tweet
    SIA = SentimentIntensityAnalyzer()
    tweets_df['polarity_score'] = tweets_df['clean_text'].apply(lambda x:SIA.polarity_scores(x)['compound'])

    return tweets_df



def wrangleData():
    tweets_df = applySentimentAnalysis(cleanData(getTweets()))
    tweets_df.to_csv("data/tweets_tidy.csv", header = True, index = False)
    return tweets_df
