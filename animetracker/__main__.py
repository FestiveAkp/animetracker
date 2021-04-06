import logging
from logging.handlers import TimedRotatingFileHandler
import os
import time

from dotenv import load_dotenv
import schedule

from animetracker.workflows import anilist_popularity

# Load environment variables and set logging
load_dotenv()
logname = 'logs/animetracker.log'
os.makedirs(os.path.dirname('logs/'), exist_ok=True)
handler = TimedRotatingFileHandler(logname, when='midnight', interval=1, encoding='utf8')
handler.suffix = '%Y-%m-%d'
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.info('Bot started')

# Schedule bot routine
schedule.every().day.at(os.environ['ANILIST_POPULARITY_START']).do(anilist_popularity)

# Run the bot
while True:
    schedule.run_pending()
    time.sleep(1)
