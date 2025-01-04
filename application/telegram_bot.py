from telegram import (
    ForceReply, 
    Update
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

class TeleBot:
    def __init__(self, telegram_bot_api):
        self.app = ApplicationBuilder().token(telegram_bot_api).build()

        self.app.add_handler(CommandHandler("start", self.command_start))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_answer))

    async def command_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )

    async def message_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("A")

    async def run_bot(self):
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

