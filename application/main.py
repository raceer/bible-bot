import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
    text="""
    Commands:
    /help - help
    /start - start
    """
    )

def main():
    load_dotenv()
    telegram_bot_api_token = os.getenv("TELEGRAM_API")
    application = ApplicationBuilder().token(telegram_bot_api_token).build()
    
    start_handler = CommandHandler('start', start)
    help_hanlder = CommandHandler("help", help)
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    application.add_handler(start_handler)
    application.add_handler(help_hanlder)
    application.add_handler(message_handler)
    
    application.run_polling()

if __name__ == '__main__':
    main()