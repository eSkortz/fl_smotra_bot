from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🚗 Автомобили", callback_data=f"cars_main")
    )
    builder.row(
        types.InlineKeyboardButton(text="🐟 Рыбалка", callback_data=f"fishing_main"),
        types.InlineKeyboardButton(text="📦 Лут-предметы", callback_data=f"loot_main"),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🛒 Торговая площадка Discord", callback_data=f"discord_main"
        )
    )
    builder.row(
        types.InlineKeyboardButton(text="🏠 Аренда ГМ", callback_data=f"rent_main")
    )
    builder.row(
        types.InlineKeyboardButton(text="📣 Поддержка", callback_data=f"support_main"),
        types.InlineKeyboardButton(text="💎 Премиум", callback_data=f"premium_main"),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="💬 Smotra Assistant chat",
            url="https://t.me/smotra_assistant",
        )
    )
    return builder.as_markup(resize_keyboard=True)
