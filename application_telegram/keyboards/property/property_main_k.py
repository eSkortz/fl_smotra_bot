from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🏘 Дома", callback_data=f"homes_menu"),
        types.InlineKeyboardButton(text="🏬 Бизнесы", callback_data=f"businesses_menu"),
    )
    builder.row(
        types.InlineKeyboardButton(text="🔙 В главное меню", callback_data="main_menu"),
    )
    return builder.as_markup(resize_keyboard=True)
