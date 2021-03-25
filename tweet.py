# %%
import os
import threading
import logging
import tweepy
import datetime
import textwrap
from dotenv import load_dotenv

import analysis
from lib.ordinal import ordinal

logger = logging.getLogger(__name__)

def schedule(changes):
    '''
    Given the result of the analysis, this will schedule the tweets to be sent in the future,
    which is done by scheduling threads that execute after some time.
    Make sure that each tweet gets a chance to be sent before the next bot cycle occurs, i.e.
    if the cycle occurs every 8 hours, tweets should be scheduled in the next 8 hours
    '''
    # Goal is to send all tweets every 24 hour cycle, one tweet now, one in 2.25 hours, etc.
    wait = 3
    for change in changes:
        logger.info(f"Queueing tweet to be sent in {datetime.timedelta(seconds=wait)} : *{change['current']['title']['romaji']}* passes *{change['surpassed']['title']['romaji']}*")
        
        # Construct tweet
        tweet = construct_popularity_change_tweet(change)

        # Create thread that waits, then sends it
        timer = threading.Timer(wait, sendTweet, [tweet])
        timer.start()

        # Increase wait between threads, so each tweet is sent 2.25 hours after each other
        wait += 8100
    
    logger.info('Tweet scheduling complete')

def construct_popularity_change_tweet(change):
    '''
    Constructs a single ranking change tweet
    '''
    current_anime = change['current']
    current_title = current_anime['title']['english'] if current_anime['title']['english'] is not None else current_anime['title']['romaji']
    current_popularity = current_anime['popularity']
    current_position = current_anime['position']
    current_url = current_anime['siteUrl']
    current_hashtags = current_anime['hashtag'] if current_anime['hashtag'] is not None else ''

    surpassed_anime = change['surpassed']
    surpassed_title = surpassed_anime['title']['english']
    surpassed_hashtags = surpassed_anime['hashtag'] if surpassed_anime['hashtag'] is not None else ''

    hashtags = '#AniList'
    if surpassed_hashtags:
        hashtags = f'{surpassed_hashtags} {hashtags}'
    if current_hashtags:
        hashtags = f'{current_hashtags} {hashtags}'

    # Build tweet
    tweet = textwrap.dedent(f'''
        *{current_title}* just passed *{surpassed_title}* in popularity on @AniListco 🎉

        It is now the {ordinal(current_position + 1)} most popular anime and has {current_popularity} members ✨

        {hashtags}

        {current_url}
    ''')

    logger.info(f'Constructed tweet:')
    logger.info(tweet)

    return tweet

def sendTweet(tweet):
    '''
    Submits a fully formed tweet to the Twitter API
    '''
    # Load environment variables
    CONSUMER_KEY = os.environ.get('TWITTER_API_KEY')
    CONSUMER_SECRET = os.environ.get('TWITTER_API_SECRET')
    ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
    ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')

    # Authorize and connect to Twitter API
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)

    # Tweet tweet
    api.update_status(tweet)

    logger.info('Tweet sent successfully')

if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    top_100_changes = analysis.top_100_popularity()
    for change in top_100_changes: 
        construct_popularity_change_tweet(change)
    # schedule(top_100_changes)
