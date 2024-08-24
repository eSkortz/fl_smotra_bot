from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🚗 Автомобили", callback_data=f"cars_main"),
        types.InlineKeyboardButton(text="🐟 Рыбалка", callback_data=f"fishing_main"),
    )
    builder.row(
        types.InlineKeyboardButton(text="🌐 Discord", callback_data=f"discord_main"),
    )
    builder.row(
        types.InlineKeyboardButton(text="🏠 Аренда ГМ", callback_data=f"rent_main"),
        types.InlineKeyboardButton(text="🏖 Мое имущество", callback_data=f"property_main")
    )
    builder.row(
        types.InlineKeyboardButton(text="💭 Поддержка", callback_data=f"support_main"),
        types.InlineKeyboardButton(text="💎 Премиум", callback_data=f"premium_main"),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="💬 SmotraAssistant chat",
            url="https://t.me/smotra_assistant",
        )
    )
    return builder.as_markup(resize_keyboard=True)
