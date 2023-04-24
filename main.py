import logging
from app.app import application


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


def main():
    application.run_polling()


if __name__ == '__main__':
    main()
