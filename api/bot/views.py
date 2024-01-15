import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from loguru import logger
from sqlalchemy.orm import Session as SessionType
from telebot import TeleBot
from telebot.types import Update
from bot import register
from api.utils.db import get_db
from core.config import settings
from core.models import User

router = APIRouter(prefix="/telegram")


@router.post(
    "/{token}",
    include_in_schema=False,
)
async def webhook(
        token: str,
        request: Request,
        db: SessionType = Depends(get_db),
):
    if token != settings.telegram_token:
        raise HTTPException(400)
    try:
        bot = TeleBot(token=token, threaded=False, parse_mode="MarkdownV2", use_class_middlewares=True)
        json_data = await request.json()
        update = Update.de_json(json_data)
        register(bot, db)
        bot.process_new_updates([update])
        return "OK"
    except Exception as exc:
        logging.error("telegram error", exc_info=exc)
        return "OK"
