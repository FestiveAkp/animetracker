# %%
import os
import requests
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def run():
    '''
    Performs the ingest routine, fetching the top 100 anime from 
    the AniList API and storing the response in our local data file
    '''
    logger.info('Running ingest...')

    API_URL = os.environ.get('ANILIST_API_URL')
    
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

        # Make the HTTP Api request
        response = requests.post(API_URL, json={'query': query, 'variables': variables})

        # Take what we need (media array) and append it to what we've got
        page = response.json()['data']['Page']['media']
        data['media'] += page
    
    FILE_NAME = os.environ.get('FILE_NAME')

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

if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    run()
