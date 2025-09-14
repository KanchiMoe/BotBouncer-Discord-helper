import logging

from src.pushshift.query_pushshift import get_posts
from src.helpers.extract_subreddits import extract_subreddit_post_pushshift

def entry(telegram_handle):
    logging.info("Searching pushshift for posts containing the TG handle: %s", telegram_handle)
    ps_data = get_posts(telegram_handle)

    # extract the subreddits
    extract_subreddit_post_pushshift(ps_data)
