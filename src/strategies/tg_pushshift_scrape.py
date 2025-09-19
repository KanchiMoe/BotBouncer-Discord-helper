import logging
import random
import time
import uuid

from src import helpers
from src import reddit

from src.pushshift.query_pushshift import get_posts

def entry(telegram_handle):
    run_uuid = uuid.uuid4()
    logging.info(f"Run UUID: {run_uuid}")

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

    not_botbouncer_banned = []

    # for each user in the list of unique users
    for user in unique_users:
        state, _ = reddit.shadowban_check(user)

        # if state is not 0 (active)
        if state != 0:
            # sleep for 1-5 seconds
            sleep_for = random.randint(1, 5)
            logging.debug(f"Sleeping for {sleep_for} seconds")
            time.sleep(sleep_for)
            continue
        
        # check to see if they have already been banned
        results = reddit.search_botbouncer(user)
        results_list = list(results)

        if results_list:
            logging.info(f"Found {len(results_list)} results for {user} on /r/BotBouncer")
            time.sleep(1)
            continue
        
        logging.info(f"Found {len(results_list)} results for {user} on /r/BotBouncer")
        not_botbouncer_banned.append(user)

        print("aaaaaaaaaa" * 20, flush=True)
        time.sleep(3)

    print("==" * 60)
    print("end of run")
    print(not_botbouncer_banned)
