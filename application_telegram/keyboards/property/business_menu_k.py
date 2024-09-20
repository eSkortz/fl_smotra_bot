from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from database.orm.public_businesses_model import Businesses


async def get(business: Businesses) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=f"♻️ Выполнил все задания",
            callback_data=f"business_refresh_tasks|{business.id}",
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=f"💸 Снял с бизнеса все деньги",
            callback_data=f"business_cash_out|{business.id}",
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=f"🗑 Удалить бизнес", callback_data=f"business_remove|{business.id}"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад к 🏬 Бизнесы", callback_data="business_list"
        ),
    )
    return builder.as_markup(resize_keyboard=True)
