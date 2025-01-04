import os, asyncio
from dotenv import load_dotenv
from counter import *
from telegram_bot import *

def main():
    load_dotenv()
    telegram_bot_api = os.getenv("TELEGRAM_API")

    app = ApplicationBuilder().token(telegram_bot_api).build()

    app.add_handler(CommandHandler("start", command_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_answer))

    app.run_polling(allowed_updates=Update.ALL_TYPES)

async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def message_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("A")

if __name__ == "__main__":
    main()
