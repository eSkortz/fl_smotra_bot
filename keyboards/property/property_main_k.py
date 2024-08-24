from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🏠 Мои дома", callback_data="my_homes"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🏦 Мои бизнесы", callback_data="my_businesses"
        )
    )
    builder.row(
        types.InlineKeyboardButton(text="🔙 В главное меню", callback_data="main_menu")
    )
    return builder.as_markup(resize_keyboard=True)
