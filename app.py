from telegram.ext import Application, CommandHandler, PicklePersistence
from .config import BOT_TOKEN


from .start import start
from .timer import timer
from .translator import get_translate_conversation_handler


async def on_init(app: Application):
    await app.bot.set_my_commands([
        ("start", "Начать работу"),
        ("timer", "Запустить таймер(формат ввода - (*s*m*h)"),
        ("translate", "Начать перевод"),
        ("stop", "Закончить перевод")
    ])


persistence = PicklePersistence(filepath="persistence.bin")
application = (
    Application
    .builder()
    .token(BOT_TOKEN)
    .persistence(persistence)
    .post_init(on_init)
    .build()
)

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("timer", timer))
application.add_handler(get_translate_conversation_handler())
