from datetime import datetime
import json
import logging
import os
import requests
import textwrap

from dotenv import load_dotenv

from ..helpers import ordinal

load_dotenv()
logger = logging.getLogger(__name__)


def ingest():
    '''
    Performs the ingest routine, fetching the top 100 anime from 
    the AniList API and storing the response in our local data file
    '''
    logger.info('Running ingest...')

    API_URL = os.environ['ANILIST_API_URL']
    
    # Define GraphQL query (grab a page of anime titles sorted by popularity)
    query = '''
        # Define which variables will be used in the query (id)
        query ($page: Int, $perPage: Int) {
            Page (page: $page, perPage: $perPage) {
                # pageInfo {
                #     total
                #     perPage
                #     currentPage
                #     lastPage
                #     hasNextPage
                # }
                media (format: TV, sort: POPULARITY_DESC) {
                    title {
                        romaji
                        english
                        native
                    }
                    season
                    seasonYear
                    popularity
                    hashtag
                    siteUrl
                    coverImage {
                        large
                    }
                }
            }
        }
    '''

    # Define new data object, which gets appended to JSON array file
    data = {
        'date': datetime.now().strftime('%m-%d-%Y %H:%M:%S'),
        'media': []
    }

    # Grab 3 pages of data from the AniList API, aka 120 shows
    # We're only tracking the top 100, but this allows some buffer at the end
    for i in range(3):
        # Define our query variables and values that will be used in the query request
        variables = {'page': i + 1, 'perPage': 40}

        # Make the HTTP API request
        response = requests.post(API_URL, json={'query': query, 'variables': variables})

        # Take what we need (media array) and append it to what we've got
        page = response.json()['data']['Page']['media']
        data['media'] += page
    
    FILE_NAME = 'al_top100_popularity.json'

    # If outfile doesn't exist, initialize one w/ empty JSON array
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w') as f:
            json.dump([], f)

    # Load stored JSON, append new data, save it back
    with open(FILE_NAME, 'r+') as f:
        store = json.load(f)
        f.seek(0)
        store.append(data)
        json.dump(store, f)
        f.truncate()


def analysis():
    '''
    Performs the top 100 popularity analysis, detecting
    changes in the ranking of each anime between the most recent
    list and the previously fetched list, returning the results
    as a list to be tweeted out
    '''
    logger.info('Performing analysis...')

    # Import data from JSON file
    FILE_NAME = 'al_top100_popularity.json'
    with open(FILE_NAME, 'r') as f:
        store = json.load(f)

    # Get latest and previous popularity ranking
    current_list = store[-1]['media']
    previous_list = store[-2]['media']

    # Check for changes in the popularity ranking
    # Iterate through latest popularity list
    results = []
    for current_position, current_anime in enumerate(current_list):
        # Only consider the first 100 shows
        if current_position > 100:
            break

        # Get current anime's previous popularity position (its index in the list)
        previous_position = 0
        for j, previous_anime in enumerate(previous_list):
            if previous_anime['title']['english'] == current_anime['title']['english']:
                previous_position = j
                break

        # Check if title moved up in popularity rankings
        if current_position < previous_position:
            current_anime['position'] = current_position

            # Keep track of results as current/surpassed tuples
            results.append((current_anime, current_list[current_position + 1]))

            logger.info(f"Discovered that *{current_anime['title']['romaji']}* passes *{current_list[current_position + 1]['title']['romaji']}*")

    return results


def make_tweet(current_anime, surpassed_anime):
    '''
    Constructs a single popularity ranking change tweet
    '''
    current_title = current_anime['title']['english'] if current_anime['title']['english'] else current_anime['title']['romaji']
    current_popularity = current_anime['popularity']
    current_position = current_anime['position']
    current_url = current_anime['siteUrl']
    current_hashtags = current_anime['hashtag'] if current_anime['hashtag'] else ''

    surpassed_title = surpassed_anime['title']['english'] if surpassed_anime['title']['english'] else surpassed_anime['title']['romaji']
    surpassed_hashtags = surpassed_anime['hashtag'] if surpassed_anime['hashtag'] else ''

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

    logger.info(f"Constructed tweet: *{current_anime['title']['romaji']}* passes *{surpassed_anime['title']['romaji']}*")

    return tweet
