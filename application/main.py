import os, asyncio
from dotenv import load_dotenv
from counter import *
from telegram_bot import *
import telegram

async def main():
    load_dotenv()
    telegram_bot_api = os.getenv("TELEGRAM_API")

    bot = telegram.Bot(telegram_bot_api)
    async with bot:
        # print(await bot.get_me())
        updates = (await bot.get_updates())
        # print(updates)
        for message in updates:
            print(message.message.text)

        print(message.message)
        user = message.message.from_user.username
        id = message.message.from_user.id
        await bot.send_message(text=f"Hi, {user}!", chat_id=id)

        
        

async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def message_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("A")

if __name__ == "__main__":
    asyncio.run(main())
