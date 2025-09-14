from dotenv import load_dotenv
import logging
import os

DEFAULT_LOG_LEVEL = os.environ.get("LOG_LEVEL") or logging.DEBUG
logging.getLogger().setLevel(DEFAULT_LOG_LEVEL)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    pass

if __name__ == "__main__":
    if not os.environ.get("NOT_DOTENV"):
        load_dotenv()

    main()
