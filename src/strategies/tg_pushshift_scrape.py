import logging

from src.pushshift.query_pushshift import get_posts
from src.helpers.extract_subreddits import extract_subreddit_post_pushshift
from src.helpers.unique_users import get_unique_users_post_pushshift

def entry(telegram_handle):
    logging.info("Searching pushshift for posts containing the TG handle: %s", telegram_handle)
    ps_data = get_posts(telegram_handle)

    # how many items did we find
    ps_item_count = len(ps_data)

    # handle if 0 items
    if ps_item_count == 0:
        logging.warning("0 posts were found by Pushshift.")
        return None
    logging.info(f"{ps_item_count} posts were found by Pushshift")

    # extract the subreddits
    extract_subreddit_post_pushshift(ps_data)

    # find unique users
    unique_users = get_unique_users_post_pushshift(ps_data)

