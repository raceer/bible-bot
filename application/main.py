from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

from dotenv import load_dotenv
import os

from counter import Counter
from sqlite_manager import DatabaseManager

class BibleBot:
    def __init__(self, token: str, database_path):
        self.token = token
        self.application = ApplicationBuilder().token(self.token).build()

        # Add command handlers
        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CommandHandler('help', self.help_command))
        self.application.add_handler(CommandHandler('set', self.set_timer))
        self.application.add_handler(CommandHandler(['unset', 'stop'], self.unset))

        # Add a message handler for general text
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))

        self.user_db = DatabaseManager(database_path)
        self.counters = {}
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command."""
        await update.message.reply_text("Hello! Welcome to the bot. How can I assist you?")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command."""
        await update.message.reply_text("Here are the commands you can use:\n/start - Start the bot\n/help - Get help")

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Echo back the user's message."""
        await update.message.reply_text(f"You said: {update.message.text}")
    
    def remove_job_if_exists(self, name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
        current_jobs = context.job_queue.get_jobs_by_name(name)
        if not current_jobs:
            return False
        for job in current_jobs:
            job.schedule_removal()
        return True
    
    async def set_timer(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.effective_message.chat_id
        chat_id_str = str(chat_id)

        self.user_db.add_user(chat_id)
        if chat_id not in self.counters:
            self.counters[chat_id_str] = Counter(0, self.user_db.get_score(chat_id))

        try:
            due = float(context.args[0])
            if due < 0:
                await update.effective_message.reply_text("Sorry we can not go back to future!")
                return

            job_removed = self.remove_job_if_exists(chat_id_str, context)
            context.job_queue.run_repeating(self.alarm, due, chat_id=chat_id, name=chat_id_str, data=self.counters[chat_id_str].retrieve_value())

            text = "Timer successfully set!"
            if job_removed:
                text += " Old one was removed."
            await update.effective_message.reply_text(text)

        except (IndexError, ValueError):
            await update.effective_message.reply_text("Usage: /set <seconds>")

    async def unset(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Remove the job if the user changed their mind."""
        chat_id = update.message.chat_id
        job_removed = self.remove_job_if_exists(str(chat_id), context)
        text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
        await update.message.reply_text(text)

    async def alarm(self, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send the alarm message."""
        job = context.job
        chat_id = job.chat_id
        data = self.counters[str(job.chat_id)].retrieve_value()
        self.user_db.update_score(chat_id, data)
        timer_limit = 10
        if data > timer_limit:
            self.counters[str(job.chat_id)].reset_counter()
            self.user_db.update_score(chat_id, self.counters[str(chat_id)].retrieve_value())
            await context.bot.send_message(job.chat_id, text="Timer is above limit, quitting.")
            self.remove_job_if_exists(str(job.chat_id), context)
        else:
            await context.bot.send_message(job.chat_id, text=f"{data}")

    def run(self):
        """Run the bot."""
        print("Bot is running...")
        self.application.run_polling()

if __name__ == "__main__":
    load_dotenv()
    telegram_bot_api_token = os.getenv("TELEGRAM_API")
    bot = BibleBot(telegram_bot_api_token, "cache/user_data.db")
    bot.run()
