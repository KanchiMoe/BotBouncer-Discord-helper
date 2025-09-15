from bs4 import BeautifulSoup
import logging
import requests

def request_handler(username: str):
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0' }
    profile_url = f"https://www.reddit.com/user/{username}/"
    
    response = requests.get(profile_url, headers=headers, allow_redirects=False)
    logging.debug(f"Response code: {response.status_code}")
        
    if response.status_code == 429:
        logging.warning("We are being ratelimited")
    
    return response

def shadowban_check(username: str):
    response = request_handler(username)
    soup = BeautifulSoup(response.text, 'html.parser')

    # live profile
    live_profile = soup.find('div', {'data-testid': 'profile-main'})
    if live_profile:
        logging.info("User %s is active.", username)
        return 0, "active"
    
    # suspended or never existed
    forbidden_title = soup.find('h1', id='shreddit-forbidden-title')
    if forbidden_title:
        title_text = forbidden_title.get_text(strip=True)

        if "has been suspended" in title_text:
            logging.info("User %s is suspended.", username)
            return 1, "suspended"
        elif "nobody on Reddit goes by that name" in title_text:
            logging.info("User %s never existed.", username)
            return 2, "deleted"
        else:
            logging.warning("Unrecognized forbidden_title text: '%s'", title_text)
            return -1, "error"

    # deleted account — more lenient text match
    deleted_header = soup.select_one('h3.font-bold.text-24.text-neutral-content-strong')
    if deleted_header:
        logging.info("User %s has deleted their account.", username)
        return 3, "deleted"

    # fallback
    logging.error("User %s returned unknown page format.", username)
    return -1, "error"
