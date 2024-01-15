from sqlalchemy.orm import Session as SessionType
from telebot import TeleBot

from bot.filters import SessionStateFilter
from bot.middleware import BotSessionMiddleware
from core.models import User
from bot.handlers import *


def register(bot: TeleBot, db: SessionType):
    bot.setup_middleware(BotSessionMiddleware(db))
    bot.add_custom_filter(SessionStateFilter(db))
    bot.register_message_handler(start, commands=["start"], pass_bot=True)
    bot.register_message_handler(search, func=lambda message: message.text == 'Поиск', pass_bot=True)
    bot.register_inline_handler(callback=search_query, func=lambda _: True, pass_bot=True)
    bot.register_chosen_inline_handler(callback=chosen_product, func=lambda _: True, pass_bot=True)
