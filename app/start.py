from telegram import ReplyKeyboardMarkup


start_keyboard = [['/translate', '/timer']]
start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=False)


async def start(update, context):
    await update.message.reply_text(
        "/translate - активировать переводчик, /timer - поставить таймер",
        reply_markup=start_markup
    )

