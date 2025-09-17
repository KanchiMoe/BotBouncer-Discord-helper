import logging
import random
import time

from src import helpers

from src.pushshift.query_pushshift import get_posts
from src.reddit.shadowban_check import shadowban_check

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
    helpers.extract_subreddit_post_pushshift(ps_data)

    # find unique users
    unique_users = helpers.get_unique_users_post_pushshift(ps_data)

    # STILL WIP
    # for each user in the list of unique users
    for user in unique_users:
        state, _ = shadowban_check(user)

        # if state is not 0 (active)
        if state != 0:
            # sleep for 1-5 seconds
            sleep_for = random.randint(1, 5)
            logging.debug(f"Sleeping for {sleep_for} seconds")
            time.sleep(sleep_for)
            continue
            
        print("=================================================================")
        print(f"{user}")
