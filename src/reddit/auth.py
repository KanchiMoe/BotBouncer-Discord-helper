import logging
import os

def get_refresh_token():
    # check we have the API key
    REDDIT_REFRESH_TOKEN = os.getenv('REDDIT_REFRESH_TOKEN')
    if not REDDIT_REFRESH_TOKEN:
        err_msg = "REDDIT_REFRESH_TOKEN is not set or empty."
        logging.critical(err_msg)
        raise RuntimeError(err_msg)

    return REDDIT_REFRESH_TOKEN

def reddit_auth_main():
    # does a refresh token exist already
    refresh_token = get_refresh_token()