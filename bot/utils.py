import re

from sqlalchemy.orm import Session as SessionType

from core.models import User


def get_user(telegram_id: str | int, db: SessionType):
    user = db.query(User).filter(User.telegram_id == str(telegram_id)).one_or_none()
    return user


def create_user(telegram_id: str | int, name: str | None, db: SessionType) -> User:
    user = User(telegram_id=telegram_id, name=name)
    db.add(user)
    db.commit()
    return user


def is_phone_number(text):
    if re.match(r'^\d{10}$', text):
        return True
    return False


def is_valid_email(text):
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', text):
        return True
    return False
