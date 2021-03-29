import logging

from dotenv import load_dotenv

from .anilist import popularity as ap
from .twitter import schedule_tweets

load_dotenv()
logger = logging.getLogger(__name__)


def anilist_popularity():
    '''
    Performs the full AniList top 100 popularity ranking analysis routine,
    periodically sending out the results as tweets afterward
    '''
    logger.info('-- Running AniList top 100 popularity routine --')
    ap.ingest()
    results = ap.analysis()
    tweets = [ap.make_tweet(current, surpassed) for current, surpassed in results]
    schedule_tweets(tweets, 2.5)
