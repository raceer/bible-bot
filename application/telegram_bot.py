from dotenv import load_dotenv
import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.application = ApplicationBuilder().token(self.token).build()

        # Add command handlers
        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CommandHandler('help', self.help_command))

        # Add a message handler for general text
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command."""
        await update.message.reply_text("Hello! Welcome to the bot. How can I assist you?")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command."""
        await update.message.reply_text("Here are the commands you can use:\n/start - Start the bot\n/help - Get help")

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Echo back the user's message."""
        await update.message.reply_text(f"You said: {update.message.text}")

    def run(self):
        """Run the bot."""
        print("Bot is running...")
        self.application.run_polling()

# Usage
if __name__ == "__main__":
    load_dotenv()
    telegram_bot_api_token = os.getenv("TELEGRAM_API")
    bot = TelegramBot(telegram_bot_api_token)
    bot.run()
