import snscrape.modules.twitter as sntwitter
import pandas as pd

# Constants
NUM_DAILY_TWEETS = 21
NUM_DAYS = 28
MIN_YR = 2012
MAX_YR = 2021
CURRENT_MONTH = 5

def scrapeTwitter():

    print("Using TwitterSearchScraper to scrape data and append tweets to list")

    # Get a certain amount of tweets for the first 28 days of each month from 2013 - 2021
    for year in range(MIN_YR, MAX_YR + 1):
        # Creating list to append tweet data to
        tweets = []
        
        for month in range(1, 13):
            # End scrapping if we have reached present day
            if (year >= MAX_YR and month > CURRENT_MONTH):
                break

            print(f"Scrapping: {year:04}-{month:02}")
            for day in range(1, NUM_DAYS + 1):
                for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'self driving cars since:{year-1}-12-31 until:{year:04}-{month:02}-{day:02}').get_items()):
                    if i >= NUM_DAILY_TWEETS:
                        break
                    tweets.append([year, month, tweet.date, tweet.content])


        #Creating a dataframe from the tweets list above
        tweets_df = pd.DataFrame(tweets, columns=['year', 'month', 'datetime', 'text'])

        print("Saving Dataframe as a csv file")
        tweets_df.to_csv(f"data/tweets_{year}.csv", header = True, index = True)



