from datetime import datetime, timedelta, timezone
import json
import logging
import os
import requests

def time_3m_ago():
    # calculate date for 3 months ago
    three_months_ago = datetime.now(timezone.utc) - timedelta(days=90)
    unix_timestamp = int(three_months_ago.timestamp())
    logging.debug("Calculated timestamp for 3 months ago: %s", three_months_ago)
    logging.debug("Calculated unix timestamp: %s", unix_timestamp)
    return unix_timestamp

def get_posts(keyword, limit=1000):
    # check we have the API key
    PS_API_KEY = os.getenv('PS_API_KEY')
    if not PS_API_KEY:
        err_msg = "PS_API_KEY is not set or empty."
        logging.critical(err_msg)
        raise RuntimeError(err_msg)

    # get timestamp for 3m ago
    unix_timestamp = time_3m_ago()

    # construct request
    PS_API_KEY = os.getenv('PS_API_KEY')
    url = "https://api.pushshift.io/reddit/submission/search"
    headers = {
        "Authorization": f"Bearer {PS_API_KEY}"
    }

    params = {
        "q": keyword,
        "size": limit,
        "after": unix_timestamp
    }

    # Send the request
    try:
        logging.debug("Submitting request to pushshift...")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        posts_raw_json = data.get("data", [])
        logging.debug("Search complete, returning...")

        # debugging
        posts_pretty_json = json.dumps(posts_raw_json, indent=2)
        #logging.debug("Json dump:")
        #logging.debug(posts_pretty_json)
    
        return posts_raw_json

    # error handling
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        raise RuntimeError
