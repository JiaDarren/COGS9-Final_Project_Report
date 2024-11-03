import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from datetime import datetime

import data_wrangling
import tweet_webscraping

MIN_YR = tweet_webscraping.MIN_YR
MAX_YR = tweet_webscraping.MAX_YR


def removeFrame(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)

    ax.spines.bottom.set_position('center')


def main():

    # Creates Explanatory visualization
    def plotCombinedLine():
        fig, ax = plt.subplots(figsize = (16,8))
        
        # Plot every single tweet's polarity score
        #ax.scatter(tweets_df["date"], tweets_df["polarity_score"], s = 0.5, color = "gray")

        # Plot daily average tweet polarity score
        #ax_1 = ax.twinx()
        ax.set_ylim(-1, 1)
        #ax.set_yticks([])
        ax.plot(day_avg["date"], day_avg["polarity_score"], color = "gray", alpha = 0.4)
        removeFrame(ax)

        # Plot monthly average polarity score
        ax_2 = ax.twinx()
        ax_2.set_ylim(-1, 1)
        ax_2.plot(month_avg["date"], month_avg["polarity_score"], linewidth = 2, color = "blue")
        ax_2.set_yticks([])
        removeFrame(ax_2)

        # Plot points where Tesla car models were released
        ax_3 = ax.twinx()
        ax_3.set_ylim(-1, 1)
        ax_3.set_yticks([])
        ax_3.scatter(releases_df["date"], [0, 0, 0, 0], s = 10, color = "red")
        removeFrame(ax_3)

        #Annotate release dates
        for index, row in releases_df.iterrows():
            plt.annotate(f"{row['model']} released on\n{row['date'].date()}", (row['date'], 0),
                         textcoords = "offset points",
                         xytext = (0, -75),
                         ha = 'center',
                         size = 10,
                         color = 'red')

        # Create titles and labels
        ax.set_title('Public Sentiment of Self-Driving Cars Stay Consistent Despite\n' +
                     'New Tesla Models Being Released',
                     size = 25,
                     ha = "left",
                     x = 0.025,
                     y = 0.9,
                     fontweight = "bold")
        ax_2.set_title('According to tweets from Twitter from 2012-2021',
                       size = 10,
                       ha = "left",
                       x = 0.025,
                       y = 0.87)
        
        ax.set_ylabel('Positive sentiment', rotation = "horizontal")
        ax.yaxis.set_label_coords(-0.1,0.95)

        ax_2.set_ylabel('Negative sentiment', rotation = "horizontal")
        ax_2.yaxis.set_label_coords(-0.1,0.05)
        ax.set_xlabel('year')


        # Make legend
        custom_lines = [Line2D([0], [0], color="gray", lw=2),
                        Line2D([0], [0], color="blue", lw=2)]
        ax.legend(custom_lines,
                  ['Daily Average Tweet Sentiment about Self-Driving Cars',
                   'Monthly Average Tweet Sentiment about Self-Driving Cars'],
                  loc = "lower left")


        # Display plot and save the figure in a file
        plt.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1)
        plt.savefig("figures/sentiment_consistent.png")
        plt.show()
    
    
    # Only run this if you want to webscrape Twitter!
    # If you have data in the data folder, DO NOT RUN!!!
    #tweet_webscraping.scrapeTwitter()    #<-- Uncomment line to webscrape
    pd.options.display.max_columns = None

    # Get Tesla Model release data
    releases_df = pd.read_csv(f"data/tesla_releases.csv", lineterminator='\n')

    # Get Tweets dataset
    try:
        tweets_df = pd.read_csv(f"data/tweets_tidy.csv", lineterminator='\n')
    except FileNotFoundError:
        print("Wrangling data")
        tweets_df = data_wrangling.wrangleData()
        print("Data wrangling finished")

    
    # Group data for explanatory visualization
    tweets_df["date"] = tweets_df["date"].apply(lambda date: datetime.strptime(date, "%Y-%m-%d"))
    releases_df["date"] = releases_df["date"].apply(lambda date: datetime.strptime(date, "%Y-%m-%d"))
    day_avg = tweets_df.groupby(["date"], as_index = False).mean()

    tweets_df["month"] = tweets_df["date"].apply(lambda date: date.month)
    tweets_df["year"] = tweets_df["date"].apply(lambda date: date.year)
    month_avg = tweets_df.groupby(["year", "month"], as_index = False).mean()
    month_avg["date"] = month_avg["year"].astype(str) + month_avg["month"].astype(str)
    month_avg["date"] = month_avg["date"].apply(lambda date: datetime.strptime(date, "%Y%m"))

    
    # Produce Descriptive statistics
    releases_df["year"] = releases_df["date"].apply(lambda date: date.year)
    year_avg = tweets_df.groupby(["year"], as_index = False).mean()
    year_avg_tesla = year_avg[[year in list(releases_df["year"]) for year in year_avg["year"]]]
    year_avg_no_tesla = year_avg[[year not in list(releases_df["year"]) for year in year_avg["year"]]]
    print(year_avg_tesla.describe())
    print(tweets_df.describe())
    
    # Plot the Data
    plotCombinedLine()
    


if __name__ == '__main__':
    main()
