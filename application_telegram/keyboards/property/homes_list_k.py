from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from typing import List

from database.orm.public_homes_model import Homes


async def get(homes_list: List[Homes]) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for homes in homes_list:
        builder.row(
            types.InlineKeyboardButton(
                text=(
                    f"🏘 {homes.name} {f'({homes.balance} руб.)' if homes.balance > -500 else '🛑 Слетел в гос.'}"
                ),
                callback_data=f"homes_info|{homes.id}",
            )
        )
    if len(homes_list) < 10:
        builder.row(
            types.InlineKeyboardButton(
                text=f"➕ Добавить новый бизнес",
                callback_data=f"add_home",
            )
        )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад к 💸 Мое имущество", callback_data="property_main"
        ),
    )
    return builder.as_markup(resize_keyboard=True)
