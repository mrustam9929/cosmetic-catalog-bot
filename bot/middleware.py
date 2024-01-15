import copy
import pdb
from typing import Union
from loguru import logger
from sqlalchemy.orm import Session as SessionType
from telebot import BaseMiddleware, StateStorageBase
from telebot.types import CallbackQuery, Message

from bot.utils import get_user, create_user
from core.models import User


class SessionContext:
    def __init__(self, db: SessionType, user: User):
        self.db = db
        self.user = user
        self.session = copy.deepcopy(user.session)

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        user = self.user
        user.session = self.session
        db = self.db
        db.add(user)
        db.commit()
        return self.session


class BotSessionMiddleware(BaseMiddleware):
    def __init__(self, db: SessionType):
        self.db = db
        self.update_sensitive = True
        self.update_types = ["message", "callback_query", "inline_query", "chosen_inline_result"]

    def pre_process_message(self, message: Message, data):
        user = get_user(message.chat.id, self.db)
        if user is None:
            user = create_user(message.chat.id, name=message.from_user.first_name, db=self.db)
        message.session = SessionContext(self.db, user)
        message.db = self.db
        message.user = user

    def pre_process_callback_query(self, query: CallbackQuery, data):
        user = get_user(query.message.chat.id, self.db)
        if user is None:
            user = create_user(query.chat.id, name=query.from_user.first_name, db=self.db)
        query.session = SessionContext(self.db, user)
        query.db = self.db
        query.user = user

    def pre_process_inline_query(self, query, data):
        query.db = self.db

    def pre_process_chosen_inline_result(self, query, data):
        query.db = self.db

    def post_process_message(self, message, data, exception):
        pass

    def post_process_inline_query(self, message, data, exception):
        pass

    def post_process_chosen_inline_result(self, message, data, exception):
        pass

    def post_process_callback_query(self, query, data, exception):
        pass
