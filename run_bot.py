from bot import register
from core.config import settings
from telebot import TeleBot
from sqlalchemy.orm import Session as SessionType

from core.database import Session


def main():
    db: SessionType = Session()
    bot = TeleBot(token=settings.telegram_token, threaded=False, parse_mode="HTML", use_class_middlewares=True)
    register(bot, db)
    bot.infinity_polling(allowed_updates=["message", "callback_query", "inline_query", "chosen_inline_result"])


if __name__ == "__main__":
    main()
