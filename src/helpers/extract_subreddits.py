import logging
import os

def extract_subreddit_post_pushshift(json_data):
    # init subreddit list
    subreddits = set()

    # for each item in json_data
    # get subreddit_name_prefixed
    # if subreddit isn't empty/null
    # add to set
    for item in json_data:
        subreddit = item.get("subreddit_name_prefixed")
        if subreddit:
            subreddits.add(subreddit)
    
    logging.info("Extracted %s unique subreddits", len(subreddits))

    #
    # save the data
    #
    # first, we need to compare what's already there
    file_path = "data_store/subreddits.txt"

    # read existing file list
    existing_subreddits = set()
    new_subreddits = []

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            existing_subreddits = set(line.strip() for line in file)

    # for each subreddit in the list of subreddits
    # if the subreddit is not in the existing list
    # add to 'new subreddits'
    for subreddit in subreddits:
        if subreddit not in existing_subreddits:
            new_subreddits.append(subreddit)

    with open(file_path, "a", encoding="utf-8") as file:
        for subreddit in new_subreddits:
            file.write(subreddit + "\n")

    logging.info("Saved %s subreddits to file.", len(new_subreddits))
