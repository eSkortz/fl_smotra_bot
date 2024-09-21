from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from typing import List

from config import database_engine_async, TELEGRAM_TOKEN
from handlers.main_h import sth_error
from keyboards.property import business_menu_k, businesses_list_k, only_to_businesses_k

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_businesses_model import Businesses
from database.orm.public_users_model import Users


router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)
bot = Bot(token=TELEGRAM_TOKEN)


class BusinessGroup(StatesGroup):
    waiting_to_name = State()
    waiting_to_profit = State()
    waiting_to_tasks_count = State()
    waiting_to_balance = State()


@router.callback_query(F.data.startswith("businesses_list"))
async def businesses_list(callback: CallbackQuery) -> None:
    try:
        user: Users = await database_worker.custom_orm_select(
            cls_from=Users,
            where_params=[Users.telegram_id == callback.message.chat.id],
            get_unpacked=True,
        )
        business_list: List[Businesses] = await database_worker.custom_orm_select(
            cls_from=Businesses,
            where_params=[Businesses.user_id == user.id],
            order_by=[Businesses.created_at.asc()],
        )
        markup_inline = businesses_list_k.get(businesses_list=business_list)

        text = (
            ">🏬 Это раздел __*Бизнесы*__, здесь отображаются бизнесы находящиеся у вас во владении\.\n\n"
            ">❗️Обратите внимание, что вам автоматически будут приходить *уведомления*, когда на вашем бизнесе будет *4/7/8 заданий*\.\n\n"
            ">❗️В первом случае о том, что он перестал приносить доход, в остальных о том, что в ближайшее время он может слететь в гос\.\n\n"
            ">❗️Актуальное количество заданий на бизнесе и его баланс можно посмотреть в списке, отображенном ниже, или в меню самого бизнеса\."
        )

        await callback.message.delete()
        await callback.message.answer(
            text=text, reply_markup=markup_inline, parse_mode=ParseMode.MARKDOWN_V2
        )
    except Exception as exception:
        await sth_error(callback.message, exception)


@router.callback_query(F.data.startswith("business_menu"))
async def business_menu(callback: CallbackQuery) -> None:
    try:
        business_id = int(callback.data.split("|")[1])
        business: Businesses = await database_worker.custom_orm_select(
            cls_from=Businesses,
            where_params=[Businesses.id == business_id],
            get_unpacked=True,
        )
        markup_inline = business_menu_k.get(business=business)

        text = (
            f">🏬 *{business.name}*\n\n"
            f">__Кол\-во заданий:__ *{business.tasks_count} шт\.*\n"
            f">__Доходность:__ *{business.profit} руб\./день*\n"
            f">__Баланс:__ *{business.balance} руб\.*"
        )

        await callback.message.delete()
        await callback.message.answer(
            text=text, reply_markup=markup_inline, parse_mode=ParseMode.MARKDOWN_V2
        )
    except Exception as exception:
        await sth_error(callback.message, exception)


@router.callback_query(F.data.startswith("business_remove"))
async def business_remove(callback: CallbackQuery) -> None:
    try:
        business_id = int(callback.data.split("|")[1])
        await database_worker.custom_delete_all(
            cls_from=Businesses, where_params=[Businesses.id == business_id]
        )
        await businesses_list(callback=callback)
    except Exception as exception:
        await sth_error(callback.message, exception)


@router.callback_query(F.data.startswith("business_refresh_tasks"))
async def business_refresh_tasks(callback: CallbackQuery) -> None:
    try:
        business_id = int(callback.data.split("|")[1])
        if business_id == 0:
            user: Users = await database_worker.custom_orm_select(
                cls_from=Users,
                where_params=[Users.telegram_id == callback.message.chat.id],
                get_unpacked=True,
            )
            business_ids: List[int] = await database_worker.custom_orm_select(
                cls_from=Businesses.id,
                where_params=[Businesses.user_id == user.id],
                order_by=[Businesses.created_at.asc()],
            )
            await database_worker.custom_orm_bulk_update(
                cls_to=Businesses,
                data=[{"id": id, "tasks_count": 0} for id in business_ids],
            )
            await businesses_list(callback=callback)
        else:
            await database_worker.custom_orm_bulk_update(
                cls_to=Businesses, data=[{"id": business_id, "tasks_count": 0}]
            )
            await business_menu(callback=callback)
    except Exception as exception:
        await sth_error(callback.message, exception)


@router.callback_query(F.data.startswith("business_cash_out"))
async def business_cash_out(callback: CallbackQuery) -> None:
    try:
        business_id = int(callback.data.split("|")[1])
        if business_id == 0:
            user: Users = await database_worker.custom_orm_select(
                cls_from=Users,
                where_params=[Users.telegram_id == callback.message.chat.id],
                get_unpacked=True,
            )
            business_ids: List[int] = await database_worker.custom_orm_select(
                cls_from=Businesses.id,
                where_params=[Businesses.user_id == user.id],
                order_by=[Businesses.created_at.asc()],
            )
            await database_worker.custom_orm_bulk_update(
                cls_to=Businesses,
                data=[{"id": id, "balance": 0} for id in business_ids],
            )
            await businesses_list(callback=callback)
        else:
            await database_worker.custom_orm_bulk_update(
                cls_to=Businesses, data=[{"id": business_id, "balance": 0}]
            )
            await business_menu(callback=callback)
    except Exception as exception:
        await sth_error(callback.message, exception)


@router.callback_query(F.data == "add_business")
async def add_business(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        await callback.message.delete()
        sent_message = await callback.message.answer(
            text="✏️ Введите название для вашего бизнеса",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await state.set_state(BusinessGroup.waiting_to_name)
        await state.update_data(id_to_delete=sent_message.message_id)
    except Exception as exception:
        await sth_error(callback.message, exception)


@router.message(BusinessGroup.waiting_to_name)
async def processing_name(message: Message, state: FSMContext) -> None:
    try:
        name = message.text

        state_data = await state.get_data()
        id_to_delete = state_data["id_to_delete"]

        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)

        sent_message = await message.answer(
            text="✏️ Введите доходность вашего бизнеса \(целое число без точек и запятых, например \- 30000\)",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await state.set_state(BusinessGroup.waiting_to_profit)
        await state.update_data(id_to_delete=sent_message.message_id, name=name)
    except Exception as exception:
        await sth_error(message, exception)


@router.message(BusinessGroup.waiting_to_profit)
async def processing_profit(message: Message, state: FSMContext) -> None:
    try:
        profit = int(message.text)

        state_data = await state.get_data()
        id_to_delete = state_data["id_to_delete"]

        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)

        sent_message = await message.answer(
            text="✏️ Введите кол\-во заданий на бизнесе в данный момент",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await state.set_state(BusinessGroup.waiting_to_tasks_count)
        await state.update_data(id_to_delete=sent_message.message_id, profit=profit)
    except Exception as exception:
        await sth_error(message, exception)


@router.message(BusinessGroup.waiting_to_tasks_count)
async def processing_tasks_count(message: Message, state: FSMContext) -> None:
    try:
        tasks_count = int(message.text)

        state_data = await state.get_data()
        id_to_delete = state_data["id_to_delete"]

        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)

        sent_message = await message.answer(
            text="✏️ Введите текущий баланс бизнеса", parse_mode=ParseMode.MARKDOWN_V2
        )
        await state.set_state(BusinessGroup.waiting_to_balance)
        await state.update_data(
            id_to_delete=sent_message.message_id, tasks_count=tasks_count
        )
    except Exception as exception:
        await sth_error(message, exception)


@router.message(BusinessGroup.waiting_to_balance)
async def processing_balance(message: Message, state: FSMContext) -> None:
    try:
        balance = int(message.text)

        state_data = await state.get_data()
        id_to_delete = state_data["id_to_delete"]
        name = state_data["name"]
        profit = state_data["profit"]
        tasks_count = state_data["tasks_count"]

        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)

        user: Users = await database_worker.custom_orm_select(
            cls_from=Users,
            where_params=[Users.telegram_id == message.chat.id],
            get_unpacked=True,
        )
        data_to_insert = {
            "user_id": user.id,
            "name": name,
            "profit": profit,
            "tasks_count": tasks_count,
            "balance": balance,
        }
        await database_worker.custom_insert(cls_to=Businesses, data=[data_to_insert])

        markup_inline = only_to_businesses_k.get()
        await message.answer(
            text=("✅ Бизнес успешно создан"),
            reply_markup=markup_inline,
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    except Exception as exception:
        await sth_error(message, exception)
