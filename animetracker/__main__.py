import logging
import os
import time

from dotenv import load_dotenv
import schedule

from .workflows import anilist_popularity

# Load environment variables and set logging
load_dotenv()
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
logging.info('Bot started')

# Schedule bot routine
schedule.every().day.at(os.environ['ANILIST_POPULARITY_START']).do(anilist_popularity)

# Run the bot
while True:
    schedule.run_pending()
    time.sleep(1)
