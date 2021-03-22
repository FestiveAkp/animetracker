# %%
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

    # Schedule tweets to be sent
    tweet.schedule(top_100_changes)

if __name__ == '__main__':
    # Load environment variables and set logging
    load_dotenv()
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
    logging.info('Bot started')

    # Schedule bot routine
    schedule.every().day.at('05:00').do(main)
    schedule.every().day.at('17:00').do(main)

    # Run the bot
    while True:
        schedule.run_pending()
        time.sleep(1)
