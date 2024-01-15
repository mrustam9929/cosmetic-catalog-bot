import pdb
from operator import and_

from loguru import logger
from sqlalchemy import func
from sqlalchemy.orm import aliased
from telebot import TeleBot
from telebot.types import Message, InlineQueryResultArticle, InputTextMessageContent, InlineQuery, ChosenInlineResult, \
    InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

from api.utils.db import get_db
from bot.text import get_text, MessageTextKey
from core.database import Session
from core.models import User, Product, SiteProduct, SiteProductHistory, Site


def start(message: Message, bot: TeleBot):
    user: User = message.user
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    search = KeyboardButton('Поиск')
    markup.add(search)
    bot.send_message(message.chat.id, get_text(MessageTextKey.START_CHAT, user.language), reply_markup=markup)

    markup = InlineKeyboardMarkup()
    switch_button = InlineKeyboardButton('Поиск', switch_inline_query_current_chat='')
    markup.add(switch_button)
    bot.send_message(message.chat.id, get_text(MessageTextKey.SEARCH, user.language), reply_markup=markup)


def search(message: Message, bot: TeleBot):
    markup = InlineKeyboardMarkup()
    switch_button = InlineKeyboardButton('Поиск', switch_inline_query_current_chat='')
    markup.add(switch_button)
    bot.send_message(message.chat.id, get_text(MessageTextKey.SEARCH, message.user.language), reply_markup=markup)


def chosen_product(result: ChosenInlineResult, bot: TeleBot):  # TODO поправить добавит db в контекст
    product_id = result.result_id
    with Session() as db:
        product = db.query(Product).where(Product.id == product_id).one_or_none()
        if product is None:
            bot.send_message(result.from_user.id, f"Продукт не найден")
        site_products = db.query(SiteProduct).where(SiteProduct.product_id == product_id).all().distinct(
            SiteProduct.site_id)
        markup = InlineKeyboardMarkup()
        for site_product in site_products:
            b = InlineKeyboardButton(text=f"{site_product.site_id} сум")  # url=site_product.site_id))
            markup.add(b)
        bot.send_message(result.from_user.id, f"{product.name_ru}", reply_markup=markup)


def search_query(query: InlineQuery, bot: TeleBot):
    results = []
    query_str = query.query.lower()
    if not query:
        products = query.db.query(Product).limit(20).all()
    else:
        products = query.db.query(Product).filter(
            (Product.name_ru.ilike(f"%{query_str}%")) |
            (Product.name_ru.ilike(f"%{query_str}%")) |
            (Product.name_ru.ilike(f"%{query_str}%"))
        ).limit(20).all()

    for product in products:
        results.append(
            InlineQueryResultArticle(
                id=str(product.id),
                title=product.name_ru,
                description=product.name_ru,
                input_message_content=InputTextMessageContent(
                    message_text=product.name_ru
                )
            )

        )
    bot.answer_inline_query(query.id, results)
