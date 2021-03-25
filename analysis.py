#!/usr/bin/env python3
import os
import json
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def top_100_popularity():
    '''
    Performs the top 100 popularity analysis, detecting
    changes in the ranking of each anime between the most recent
    list and the previously fetched list, returning the results
    as a list to be tweeted out
    '''
    logger.info('Performing analysis...')

    # Import data from JSON file
    FILE_NAME = os.environ.get('FILE_NAME')
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

        # Store current anime's title
        title = current_anime['title']['english']

        # Get current anime's previous popularity position (its index in the list)
        previous_position = 0
        for j, previous_anime in enumerate(previous_list):
            if previous_anime['title']['english'] == title:
                previous_position = j
                break

        # Check if title moved up in popularity rankings
        if current_position < previous_position:
            current_anime['position'] = current_position
            current_list[previous_position]['position'] = previous_position

            # Keep track of results as current/surpassed tuples
            results.append((current_anime, current_list[previous_position]))

            logger.info(f"Discovered that *{current_anime['title']['romaji']}* passes *{current_list[previous_position]['title']['romaji']}*")

    return results

if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    r = top_100_popularity()
