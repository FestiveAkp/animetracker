# %%
import os
import json

from dotenv import load_dotenv

from lib.ordinal import ordinal

load_dotenv()
FILE_NAME = os.environ.get('FILE_NAME')

# Import data from JSON file
with open(FILE_NAME, 'r') as f:
    store = json.load(f)

# Get latest and previous popularity ranking
current_list = store[-1]['data']['Page']['media']
previous_list = store[-2]['data']['Page']['media']

# Check for changes in the popularity ranking
# Iterate through latest popularity list
for current_position, anime in enumerate(current_list):
    # Store current anime's title and position
    title = anime['title']['english']

    # Get current anime's previous popularity position (its index in the list)
    previous_position = 0
    for j, anime in enumerate(previous_list):
        if anime['title']['english'] == title:
            previous_position = j
            break

    # Check if title moved up in popularity rankings
    if current_position < previous_position:
        current_popularity = anime['popularity']
        current_url = anime['siteUrl']
        current_hashtags = anime['hashtag'] if anime['hashtag'] is not None else ''

        surpassed_anime = current_list[previous_position]
        surpassed_title = surpassed_anime['title']['english']
        surpassed_hashtags = surpassed_anime['hashtag'] if surpassed_anime['hashtag'] is not None else ''
        
        tweet = f'''
*{title}* just passed *{surpassed_title}* in popularity on #AniList 🎉

It is now the {ordinal(current_position + 1)} most popular anime and has {current_popularity} members ✨

{current_hashtags} {surpassed_hashtags}

{current_url}
        '''

        print(tweet)
        print('\n')
