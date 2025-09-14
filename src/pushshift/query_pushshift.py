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
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        posts_raw_json = data.get("data", [])
        posts_pretty_json = json.dumps(posts_raw_json, indent=2)
        return posts_pretty_json

    # error handling
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        raise RuntimeError
