# Anime Tracker 

A Twitter bot that pulls anime data from various sources daily and analyzes it, periodically tweeting out the results afterward. 

## Current Statistics
Currently tracking the Top 100 anime on AniList by popularity, detecting when shows rise in the rankings and tweeting it out.

## Installation
First, copy the `.env.example` file and configure your environment variables:
```bash
$ cp .env.example .env
```

Install Python dependencies:
```bash
$ pip3 install -r requirements.txt
```

Run the bot:
```bash
$ python3 -m animetracker
```

To run a single file (for debugging), add an `if __name__ == '__main__'` at the bottom and do:
```bash
$ python3 -m animetracker.<path>.<to>.<file>
```
