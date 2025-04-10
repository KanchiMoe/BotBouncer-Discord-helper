import discord
from discord import app_commands
import logging
import os
import praw
import prawcore
from urllib.parse import urlparse

def get_username_from_url(url):
    logging.info("Extracting username from URL...")

    # Parse the URL
    parsed_url = urlparse(url)
    
    # Check if the URL path matches the pattern for Reddit user profiles
    if parsed_url.netloc == 'www.reddit.com' and parsed_url.path.startswith('/user/'):
        # Extract username from the URL path
        username = parsed_url.path.split('/')[2]  # Assumes /user/<username> pattern
        
        # Prepare the full URL
        fullurl = f"https://www.reddit.com/user/{username}"
        
        # Return a set with the required keys
        return {"fullurl": fullurl, "username": username}
    else:
        logging.error("URL doesn't match expected pattern")
        return None

def get_reddit_client():
    logging.info("Getting reddit client")

    reddit_client = praw.Reddit(

        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        username=os.getenv('REDDIT_USERNAME'),
        password=os.getenv('REDDIT_PASSWORD'),
        user_agent=f'{os.getenv('REDDIT_USERNAME')}-botbouncer-assistant',
        check_for_async=False
    )

    logging.debug("Returning reddit client")
    return reddit_client

def is_shadowbanned(username: str, reddit_client):
    logging.info(f"Getting reddit profile for: {username}")

    try:
        user = reddit_client.redditor(username)
        _ = user.id
        logging.info(f"User: {username} not shadowbanned")
        return False
    except prawcore.exceptions.NotFound:
        logging.info(f"User: {username} IS shadowbanned")
        return True
    except Exception as e:
        logging.error(f"Some other error occurred {e}")
        return None

def ban_user(reddit_client, username):
    subreddit = reddit_client.subreddit(os.getenv('SUBREDDIT'))

    ban_username = username
    ban_duration = 365
    ban_reason = "bot"
    ban_message = """#**If human, please reply to this message.**\n
*****\n
_This action was done with the help of a script._
"""
    subreddit.banned.add(
        username,
        ban_reason=ban_reason,
        duration=ban_duration,
        ban_message=ban_message,
    )

    logging.info(f"Banned user: {ban_username}, duration: {ban_duration} days")

def report_user(reddit_client, profile: str):
    subreddit = reddit_client.subreddit("BotBouncer")

    submission = subreddit.submit(
        title=profile["username"],
        url=profile["fullurl"]
    )

@app_commands.command(name="banbot", description="Bans a user from the subreddit, and reports them to /r/botbouncer")
async def banbot(interaction: discord.Interaction, url: str):
    logging.info(f"Got paramater value: {url}")

    reddit_user = get_username_from_url(url)
    
    reddit_client = get_reddit_client()
    shadowbanned = is_shadowbanned(reddit_user["username"], reddit_client)

    ban_user(reddit_client, reddit_user["username"])
 
    if shadowbanned is True:
        return
    
    report_user(reddit_client, reddit_user)
