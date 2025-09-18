import logging
import os
import praw

def get_refresh_token():
    # check we have the API key
    REDDIT_REFRESH_TOKEN = os.getenv('REDDIT_REFRESH_TOKEN')
    if not REDDIT_REFRESH_TOKEN:
        err_msg = "REDDIT_REFRESH_TOKEN is not set or empty."
        logging.critical(err_msg)
        raise RuntimeError(err_msg)

    return REDDIT_REFRESH_TOKEN

def get_reddit_client(refresh_token=None, redirect_uri=None):
    kwargs = dict(
        client_id     = os.getenv('REDDIT_CLIENT_ID'),
        client_secret = os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent    = os.getenv('REDDIT_USER_AGENT')
    )

    if refresh_token:
        kwargs.update(refresh_token=refresh_token)
    elif redirect_uri:
        kwargs.update(redirect_uri=redirect_uri)

    return praw.Reddit(**kwargs)

def build_and_verify_reddit_client(refresh_token: str):
    reddit = get_reddit_client(refresh_token=refresh_token)

    try:
        me = reddit.user.me()
        logging.info(f"Successfully authenticated as: u/{me}")
        return reddit
    except Exception as e:
        logging.error(f"Refresh token failed: {e}")
        return None

def reddit_auth_main():
    # does a refresh token exist already
    refresh_token = get_refresh_token()

    # do this if we have a token
    if refresh_token:
        logging.debug("We have a refresh token. Trying to authenticate...")

        authed_reddit_client = build_and_verify_reddit_client(refresh_token)

        if authed_reddit_client:
            logging.debug("Reddit client is authorised. Returning it...")
            return authed_reddit_client
        else:
            # TO DO on this line, remove the existing refresh token
            #logging.info("Deleted bad refresh token. Restarting auth flow")
            logging.critical("YOU NEED TO DELETE THE REFRESH TOKEN BEFORE YOU CAN CONTINUE")
