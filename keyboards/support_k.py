from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🔙 В главное меню", callback_data="main_menu"),
        types.InlineKeyboardButton(text="📝 SA chat", url='https://t.me/smotra_assistant'),
    )
    return builder.as_markup(resize_keyboard=True)