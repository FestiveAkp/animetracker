# %%
import threading
import schedule
import time
from dotenv import load_dotenv

import ingest
import analysis
import tweet

def main():
    print('Running ingest...')
    ingest.run()

    print('Performing analysis...')
    top_100_changes = analysis.top_100_popularity()

    # Send at maximum three tweets, one now, one in 3 hours, and another in 6 hours
    wait = 1
    for i in range(3):
        if i >= len(top_100_changes):
            break

        # Create thread that waits, then sends a tweet
        print('Queueing tweet...')
        timer = threading.Timer(wait, tweet.popularity_change, [top_100_changes[i]])
        timer.start()

        # Increase wait between threads, so each tweet is sent 3 hours after each other
        wait += 10800
    
    print('Done.')

if __name__ == '__main__':
    # Load environment variables
    load_dotenv()

    # Schedule bot routine
    schedule.every(8).hours.do(main)

    # Run the bot
    while True:
        schedule.run_pending()
        time.sleep(1)
