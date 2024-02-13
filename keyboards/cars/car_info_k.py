from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from utils.text_utils import CARS_CLASSIFICATION


def get(car_mark: str, page_index: int) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=f"🔙 Назад к {CARS_CLASSIFICATION[car_mark]['emoji']} {CARS_CLASSIFICATION[car_mark]['name']}",
            callback_data=f"car_marks|{car_mark}|{page_index}",
        )
    )
    return builder.as_markup(resize_keyboard=True)
