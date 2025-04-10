import os
import logging
from dotenv import load_dotenv
from src.discordbot import BOT

load_dotenv()

DEFAULT_LOG_LEVEL = os.environ.get("LOG_LEVEL") or logging.INFO
logging.getLogger().setLevel(DEFAULT_LOG_LEVEL)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

def main():
    logging.info("Starting discord bot...")
    BOT.run(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    main()
    