from telegram_bot import TelegramBot
from counter import Counter

from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    telegram_bot_api_token = os.getenv("TELEGRAM_API")
    bot = TelegramBot(telegram_bot_api_token)
    bot.run()

if __name__ == "__main__":
    main()