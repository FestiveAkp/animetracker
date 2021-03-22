# %%
import os
import json
from dotenv import load_dotenv

def top_100_popularity():
    '''
    Performs the top 100 popularity analysis, detecting
    changes in the ranking of each anime between the most recent
    list and the previously fetched list, returning the results
    as a list to be tweeted out
    '''
    print('Performing analysis...')

    FILE_NAME = os.environ.get('FILE_NAME')

    # Import data from JSON file
    with open(FILE_NAME, 'r') as f:
        store = json.load(f)

    # Get latest and previous popularity ranking
    current_list = store[-1]['media']
    previous_list = store[-2]['media']

    # Check for changes in the popularity ranking
    # Iterate through latest popularity list
    result_list = []
    for current_position, current_anime in enumerate(current_list):
        # Store current anime's title
        title = current_anime['title']['english']

        # Get current anime's previous popularity position (its index in the list)
        previous_position = 0
        for j, current_anime in enumerate(previous_list):
            if current_anime['title']['english'] == title:
                previous_position = j
                break

        # Check if title moved up in popularity rankings
        if current_position < previous_position:
            current_anime['position'] = current_position
            current_list[previous_position]['position'] = previous_position

            result_list.append({
                'current': current_anime,
                'surpassed': current_list[previous_position]
            })
    
    print('Done.')

    return result_list

if __name__ == '__main__':
    load_dotenv()

    r = top_100_popularity()
    print(r)
