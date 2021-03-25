# %%
import os
import schedule
import time
import logging
from dotenv import load_dotenv

import ingest
import analysis
import tweet

def main():
    # Ingest data from AniList API
    ingest.run()

    # Perform analysis
    top_100_changes = analysis.top_100_popularity()

    # Create tweets
    top_100_tweets = [tweet.construct_popularity_change_tweet(current, surpassed) for current, surpassed in top_100_changes]

    # Schedule tweets to be sent
    tweet.schedule(top_100_tweets, 2.25)

if __name__ == '__main__':
    # Load environment variables and set logging
    load_dotenv()
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    logging.info('Bot started')

    # Schedule bot routine
    START_TIME = os.environ.get('START_TIME')
    schedule.every().day.at(START_TIME).do(main)

    # Run the bot
    while True:
        schedule.run_pending()
        time.sleep(1)
