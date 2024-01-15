from sqlalchemy.orm import Session as SessionType
from telebot.custom_filters import AdvancedCustomFilter
from telebot.types import CallbackQuery, Message


class SessionStateFilter(AdvancedCustomFilter):
    key = "state"

    def __init__(self, db: SessionType):
        self.db = db

    def check(self, check: Message | CallbackQuery, text: str) -> bool:
        with check.session as data:
            if text == "*":
                return True
            elif "state" in data and type(text) is list:
                return data["state"] in text
            elif "state" in data and data["state"] == text:
                return True
            return False
