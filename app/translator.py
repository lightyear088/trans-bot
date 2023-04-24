from itertools import zip_longest

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackContext, ConversationHandler, CommandHandler, MessageHandler, CallbackQueryHandler, filters
)

from .flags import get_flag_by_code
from .translator_api import get_languages, translate

SELECTING, TRANSLATION, STOP_TRANSLATION = range(3)


async def start_translate(update: Update, context: CallbackContext):
    languages = await get_languages()
    keyboard = [
        [InlineKeyboardButton(get_flag_by_code(code), callback_data=code) for code in row]
        for row in list(
            map(
                lambda x: list(filter(bool, x)),
                zip_longest(*[iter(languages)] * 4, fillvalue=None)
            )
        )
    ]
    message = await update.message.reply_text("Выберите язык", reply_markup=InlineKeyboardMarkup(keyboard))
    context.user_data["message"] = message
    return SELECTING


async def select_translate(update: Update, context: CallbackContext):
    await update.callback_query.message.edit_text(
        f"Введите текст, чтобы перевести.\nВыбранный язык: {update.callback_query.data}"
    )
    context.user_data["language"] = update.callback_query.data
    return TRANSLATION


async def do_translate(update: Update, context: CallbackContext):
    text = await translate(update.message.text, context.user_data["language"])
    await update.message.reply_text(text)
    return TRANSLATION


async def stop_translate(update: Update, context: CallbackContext):
    await context.user_data["message"].delete()
    await update.message.reply_text("Перевод окончен")
    return ConversationHandler.END


def get_translate_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("translate", start_translate)],
        states={
            SELECTING: [CallbackQueryHandler(select_translate)],
            TRANSLATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, do_translate)],
            STOP_TRANSLATION: [CommandHandler("stop", stop_translate)]
        },
        fallbacks=[CommandHandler("stop", stop_translate), CommandHandler("translate", start_translate)],
        name="translation_conversation",
        persistent=True
    )
