async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Hi! Use /set <seconds> to set a timer")


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    data = counters[str(job.chat_id)].retrieve_value()
    await context.bot.send_message(job.chat_id, text=f"Beep! {data} seconds are over!")


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    print(current_jobs)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def my_alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Beep! {job.data}")

async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    global counters
    chat_id = update.effective_message.chat_id
    counters = {}
    chat_id_str = str(chat_id)
    if chat_id not in counters:
        counters[chat_id_str] = Counter()
    
    try:
        # args[0] should contain the time for the timer in seconds
        due = float(context.args[0])
        if due < 0:
            await update.effective_message.reply_text("Sorry we can not go back to future!")
            return

        # print(counters[chat_id_str])
        job_removed = remove_job_if_exists(str(chat_id), context)
        # context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)
        context.job_queue.run_repeating(alarm, due, chat_id=chat_id, name=str(chat_id), data=counters[chat_id_str].retrieve_value())
        # context.job_queue.run_daily(alarm, 5, chat_id=chat_id, name=str(chat_id), data=counter.re)

        text = "Timer successfully set!"
        if job_removed:
            text += " Old one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <seconds>")


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
    await update.message.reply_text(text)