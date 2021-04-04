# Anime Tracker 

A Twitter bot that pulls anime data from various sources daily and analyzes it, periodically tweeting out the results afterward. 

## Current Statistics
Currently tracking the Top 100 anime on AniList by popularity, detecting when shows rise in the rankings and tweeting it out.

## Installation
First, copy the `.env.example` file and configure your environment variables:
```bash
$ cp .env.example .env
```

To run the bot, install dependencies and run:
```bash
$ python3 -m animetracker
```

To run a single file (for debugging), add an `if __name__ == '__main__'` at the bottom and do:
```bash
$ python3 -m animetracker.<path>.<to>.<file>
```
