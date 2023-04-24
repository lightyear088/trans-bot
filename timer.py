import asyncio
import re
from datetime import timedelta

from telegram import Update
from telegram.ext import CallbackContext


async def background_task(update: Update, delta: timedelta):
    await asyncio.sleep(delta.seconds)
    await update.message.reply_text("Время истекло💣")


async def timer(update: Update, context: CallbackContext):
    pattern = r"^(\d+)([smh])$"
    if len(context.args) != 1 or not re.fullmatch(pattern, context.args[0]):
        await update.message.reply_text("Неверный формат времени\nИспользуйте /timer 10m")
        return

    value, units = re.findall(pattern, context.args[0])[0]
    key = {
        "s": "seconds",
        "m": "minutes",
        "h": "hours"
    }[units]
    delta = timedelta(**{
        key: int(value)
    })
    asyncio.create_task(background_task(update, delta))
    await update.message.reply_text(f"Уведомление придёт через {delta.seconds} секунд⏳")
