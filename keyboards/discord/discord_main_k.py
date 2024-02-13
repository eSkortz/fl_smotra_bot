from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='📢 Мои объявления в Discord', callback_data="my_adds"
    ))
    builder.row(types.InlineKeyboardButton(
        text='🔔 Мои теги для уведомлений', callback_data="my_notify"
    ))
    builder.row(
        types.InlineKeyboardButton(text='🔐 Изменить Authorization', callback_data="change_authorization"),
        types.InlineKeyboardButton(text='❓ Как найти Authorization header', url='https://teletype.in/@akikora/FI4jHmqTp6s')
    )
    builder.row(types.InlineKeyboardButton(
        text='🔙 В главное меню', callback_data="main_menu"
    ))
    return builder.as_markup(resize_keyboard=True)