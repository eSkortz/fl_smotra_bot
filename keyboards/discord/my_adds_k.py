from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram.types import Message
from config import engine_async
from db.oop.alchemy_di_async import DBWorkerAsync
from db.orm.schema_public import Users, UserPointers
from utils.text_utils import BOOL_TO_STATUS_ADDS

db_worker = DBWorkerAsync(engine_async)

async def get(message: Message) -> ReplyKeyboardMarkup:

    user_id = await db_worker.custom_orm_select(cls_from=Users.id, where_params=[Users.telegram_id == message.chat.id])
    user_id = user_id[0]
    user_pointers = await db_worker.custom_orm_select(cls_from=UserPointers, where_params=[UserPointers.user_id == user_id])
    user_pointers: UserPointers = user_pointers[0]

    builder = InlineKeyboardBuilder()

    builder.row(types.InlineKeyboardButton(
        text=f'🚗 Транспорт {BOOL_TO_STATUS_ADDS[user_pointers.transport_pointer]}', callback_data="discord_my_add|transport"
    ))
    builder.row(types.InlineKeyboardButton(
        text=f'🎱 Номера {BOOL_TO_STATUS_ADDS[user_pointers.numbers_pointer]}', callback_data="discord_my_add|numbers"
    ))
    builder.row(types.InlineKeyboardButton(
        text=f'🏠 Дома {BOOL_TO_STATUS_ADDS[user_pointers.homes_pointer]}', callback_data="discord_my_add|homes"
    ))
    builder.row(types.InlineKeyboardButton(
        text=f'🏦 Бизнесы {BOOL_TO_STATUS_ADDS[user_pointers.business_pointer]}', callback_data="discord_my_add|business"
    ))
    builder.row(types.InlineKeyboardButton(
        text=f'🥋 Одежда {BOOL_TO_STATUS_ADDS[user_pointers.clothes_pointer]}', callback_data="discord_my_add|clothes"
    ))
    builder.row(types.InlineKeyboardButton(
        text=f'🔫 Оружие {BOOL_TO_STATUS_ADDS[user_pointers.weapon_pointer]}', callback_data="discord_my_add|weapon"
    ))
    builder.row(types.InlineKeyboardButton(
        text=f'📦 Лут-предметы {BOOL_TO_STATUS_ADDS[user_pointers.loot_pointer]}', callback_data="discord_my_add|loot"
    ))
    builder.row(types.InlineKeyboardButton(
        text=f'💵 Услуги {BOOL_TO_STATUS_ADDS[user_pointers.services_pointer]}', callback_data="discord_my_add|services"
    ))
    builder.row(types.InlineKeyboardButton(
        text=f'📊 Торговая общий {BOOL_TO_STATUS_ADDS[user_pointers.global_pointer]}', callback_data="discord_my_add|global"
    ))

    builder.row(types.InlineKeyboardButton(
        text='🔙 В раздел Discord', callback_data="discord_main"
    ))
    return builder.as_markup(resize_keyboard=True)