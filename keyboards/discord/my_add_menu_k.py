from aiogram.types import ReplyKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get(chapter: str) -> ReplyKeyboardMarkup:

    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="⏰ Изменить таймер", callback_data=f"change_timer|{chapter}"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="♻ Вкл/Выкл объявление", callback_data=f"add_on_off|{chapter}"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="📝 Отредактировать текст объявления",
            callback_data=f"add_change_text|{chapter}",
        ),
        types.InlineKeyboardButton(
            text="🎑 Добавить фото к объявлению",
            callback_data=f"add_attach_photo|{chapter}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🧨 Удалить все фото", callback_data=f"add_remove_photos|{chapter}"
        ),
        types.InlineKeyboardButton(
            text="🗂 Показать все фото объявления",
            callback_data=f"add_show_photos|{chapter}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад к 📢 Мои объявления", callback_data="my_adds"
        )
    )
    return builder.as_markup(resize_keyboard=True)
