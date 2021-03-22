# %%
import os
import tweepy
from datetime import datetime

from lib.ordinal import ordinal

def popularity_change(change):
    # Load environment variables
    CONSUMER_KEY = os.environ.get('TWITTER_API_KEY')
    CONSUMER_SECRET = os.environ.get('TWITTER_API_SECRET')
    ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
    ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')

    # Authorize and connect to Twitter API
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)

    # public_tweets = api.home_timeline()
    # for tweet in public_tweets:
    #     print(tweet.text)

    current_anime = change['current']
    current_title = current_anime['title']['english'] if current_anime['title']['english'] is not None else current_anime['title']['romaji']
    current_popularity = current_anime['popularity']
    current_position = current_anime['position']
    current_url = current_anime['siteUrl']
    current_hashtags = current_anime['hashtag'] if current_anime['hashtag'] is not None else ''

    surpassed_anime = change['surpassed']
    surpassed_title = surpassed_anime['title']['english']
    surpassed_hashtags = surpassed_anime['hashtag'] if surpassed_anime['hashtag'] is not None else ''

    tweet = f'''
*{current_title}* just passed *{surpassed_title}* in popularity on #AniList 🎉

It is now the {ordinal(current_position + 1)} most popular anime and has {current_popularity} members ✨

{current_hashtags} {surpassed_hashtags}

{current_url}
    '''

    current_datetime = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
    print(f'Tweeted at {current_datetime}')
    print(tweet)

if __name__ == '__main__':
    from dotenv import load_dotenv
    import analysis

    load_dotenv()
    top_100_changes = analysis.top_100_popularity()
    for change in top_100_changes:
        popularity_change(change)
