import datetime
import logging
import os
import threading

from dotenv import load_dotenv
import tweepy

load_dotenv()
logger = logging.getLogger(__name__)


def send_tweet(tweet):
    '''
    Submits a fully formed tweet to the Twitter API
    '''
    # Load API keys
    CONSUMER_KEY = os.environ['TWITTER_API_KEY']
    CONSUMER_SECRET = os.environ['TWITTER_API_SECRET']
    ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
    ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']

    # Authorize and connect to Twitter API
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)

    # Tweet tweet
    api.update_status(tweet)

    logger.info('Tweet sent successfully:')
    logger.info(tweet)


def schedule_tweets(tweets, interval):
    '''
    Given a list of tweets, this will schedule them to be sent in the future,
    which is done by scheduling threads that execute after some time, spacing
    out the tweets by the specified interval
    '''
    wait = 2
    interval_seconds = interval * 60 * 60
    
    for i, tweet in enumerate(tweets):
        logger.info(f'Queueing tweet {i} to be sent in {datetime.timedelta(seconds=wait)}')

        # Create thread that waits, then sends it
        timer = threading.Timer(wait, send_tweet, [tweet])
        timer.start()

        # Increase wait between threads, so each tweet is sent a few hours after each other
        wait += interval_seconds
    
    logger.info('Scheduling complete')
