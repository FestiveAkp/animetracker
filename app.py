# %%
import schedule
import time
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
    # Load environment variables
    load_dotenv()

    # Schedule bot routine
    schedule.every(8).hours.do(main)

    # Run the bot
    while True:
        schedule.run_pending()
        time.sleep(1)
