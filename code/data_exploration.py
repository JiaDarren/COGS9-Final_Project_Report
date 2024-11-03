import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from datetime import datetime

import data_wrangling
import tweet_webscraping

MIN_YR = tweet_webscraping.MIN_YR
MAX_YR = tweet_webscraping.MAX_YR

    
def plotAllTweetsScatter(releases_df, tweets_df, ax):
    ax.scatter(x = tweets_df['date'], y = tweets_df['polarity_score'], s = 0.5)
    ax.set_title('Polarity score of all tweets over time')
    ax.set_ylabel('polarity score')
    ax.set_xlabel('year')
    ax.set_ylim(-1, 1)

    plotTeslaReleases(releases_df, ax)
    makeLegend(ax, 'Tweet')

def plotAllTweetsDensity(tweets_df, ax1, ax2):
    # remove entires with a 0 as polarity score
    tweets_no_0 = tweets_df[tweets_df['polarity_score'] != 0.0]
    
    ax1.hist(tweets_df['polarity_score'], bins = 20)
    ax1.set_ylabel('number of tweets')
    ax1.set_xlabel('polarity score')
    ax1.set_xlim(-1, 1)
    ax1.set_title('Frequency of Polarity scores of all tweets')

    ax2.hist(tweets_no_0['polarity_score'], bins = 20)
    ax2.set_ylabel('number of tweets')
    ax2.set_xlabel('polarity score')
    ax2.set_xlim(-1, 1)
    ax2.set_title('Frequency of Polarity scores of all opinionated tweets')

def plotDailyTweets(releases_df, day_means_df, ax):
    ax.plot(day_means_df['date'], day_means_df['polarity_score'])
    ax.set_title('Daily Average of polarity score of tweets over time')
    ax.set_ylabel('polarity score')
    ax.set_xlabel('year')
    ax.set_ylim(-1, 1)

    plotTeslaReleases(releases_df, ax)
    makeLegend(ax, 'Daily average tweet polarity score')

def plotMonthlyTweets(releases_df, month_means_df, ax):
    print(month_means_df)
    ax.plot(month_means_df["date"], month_means_df['polarity_score'])
    ax.set_title('Average Monthly Polarity Score for Tweets about Self-Driving Cars')
    ax.set_ylabel('polarity score')
    ax.set_xlabel('year')
    ax.set_ylim(-1, 1)
    
    ax_3 = ax.twinx()
    ax_3.set_ylim(-1, 1)
    ax_3.set_yticks([])
    ax_3.scatter(releases_df["date"], [0, 0, 0, 0], s = 10, color = "red")

    makeLegend(ax, 'Average monthly tweet')


def plotTeslaReleases(releases_df, ax):
    ax_3 = ax.twinx()
    ax_3.set_ylim(-1, 1)
    ax_3.set_yticks([])
    ax_3.scatter(releases_df["date"], [0, 0, 0, 0], s = 10, color = "red")

def makeLegend(ax, msg):
    # Make legend
    custom_lines = [Line2D([0], [0], color="blue", lw=2),
                    Line2D([0], [0], color="red", lw=2)]
    ax.legend(custom_lines, [msg, 'Tesla model release dates'])
    

def main():
    # Only run this if you want to webscrape Twitter!
    # If you have data in the data folder, DO NOT RUN!!!
    #tweet_webscraping.scrapeTwitter()    #<-- Uncomment line to webscrape

    # Get Tesla Model release data
    releases_df = pd.read_csv(f"data/tesla_releases.csv", lineterminator='\n')
    releases_df["date"] = releases_df["date"].apply(lambda date: datetime.strptime(date, "%Y-%m-%d"))

    # Get Tweets dataset
    try:
        tweets_df = pd.read_csv(f"data/tweets_tidy.csv", lineterminator='\n')
    except FileNotFoundError:
        print("Wrangling data")
        tweets_df = data_wrangling.wrangleData()
        print("Data wrangling finished")

    tweets_df["date"] = tweets_df["date"].apply(lambda date: datetime.strptime(date, "%Y-%m-%d"))

    
    # Group each category by day
    day_avg = tweets_df.groupby(["date"], as_index = False).mean()

    # Group each category by month
    tweets_df["month"] = tweets_df["date"].apply(lambda date: date.month)
    tweets_df["year"] = tweets_df["date"].apply(lambda date: date.year)
    month_avg = tweets_df.groupby(["year", "month"], as_index = False).mean()
    month_avg["date"] = month_avg["year"].astype(str) + month_avg["month"].astype(str)
    month_avg["date"] = month_avg["date"].apply(lambda date: datetime.strptime(date, "%Y%m"))
    


    # Display Table
    pd.options.display.max_columns = None


    # Plot the Data
    #fig, (ax1, ax2) = plt.subplots(2)
    fig, ax = plt.subplots()

    #plotDailyTweets(releases_df, day_avg, ax)
    plotMonthlyTweets(releases_df, month_avg, ax)
    #plotAllTweetsScatter(releases_df, tweets_df, ax)

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
