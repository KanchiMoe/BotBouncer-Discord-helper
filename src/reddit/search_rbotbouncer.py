import logging
import json

from src.reddit.auth import reddit_auth_main

def search_botbouncer(username: str):
    logging.debug(f"Searching /r/botbouncer for {username}")

    # get reddit client
    reddit = reddit_auth_main()
    subreddit = reddit.subreddit("BotBouncer")

    # get results from reddit
    results = subreddit.search(query=f'{username}', sort='new', limit=5, params={'include_over_18': 'on'})

    return results    
