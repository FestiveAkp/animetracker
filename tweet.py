# %%
import os
import threading
import logging
import tweepy
import datetime
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
    # Goal is to send 5 tweets every 12 hour cycle, one tweet now, one in 2.25 hours, etc.
    # print(f'Current time is {datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")}')
    wait = 3
    for i in range(5):
        if i >= len(changes):
            break

        # Create thread that waits, then sends a tweet
        logger.info(f"Queueing tweet to be sent in {datetime.timedelta(seconds=wait)} : *{changes[i]['current']['title']['romaji']}* passes *{changes[i]['surpassed']['title']['romaji']}*")
        timer = threading.Timer(wait, popularity_change, [changes[i]])
        timer.start()

        # Increase wait between threads, so each tweet is sent 2.25 hours after each other
        wait += 8100
    
    logger.info('Tweet scheduling complete')

def popularity_change(change):
    '''
    Constructs a single ranking change tweet and posts it using the Twitter API
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

    # Get analysis data for tweet
    current_anime = change['current']
    current_title = current_anime['title']['english'] if current_anime['title']['english'] is not None else current_anime['title']['romaji']
    current_popularity = current_anime['popularity']
    current_position = current_anime['position']
    current_url = current_anime['siteUrl']
    current_hashtags = current_anime['hashtag'] if current_anime['hashtag'] is not None else ''

    surpassed_anime = change['surpassed']
    surpassed_title = surpassed_anime['title']['english']
    surpassed_hashtags = surpassed_anime['hashtag'] if surpassed_anime['hashtag'] is not None else ''

    # Build tweet
    tweet = f'''
*{current_title}* just passed *{surpassed_title}* in popularity on @AniListco 🎉

It is now the {ordinal(current_position + 1)} most popular anime and has {current_popularity} members ✨

#AniList {current_hashtags} {surpassed_hashtags}

{current_url}
    '''

    # Tweet tweet
    api.update_status(tweet)

    current_datetime = datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S')
    logger.info(f'Just tweeted:')
    logger.info(tweet)

if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    top_100_changes = analysis.top_100_popularity()
    schedule(top_100_changes)
