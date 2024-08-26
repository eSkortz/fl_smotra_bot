from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from datetime import datetime

from config import engine_async, BOT_TOKEN
from db.oop.alchemy_di_async import DBWorkerAsync
from db.orm.schema_public import Users, RentAdds

from handlers.main_h import sth_error
from handlers.rent.my_rents_h import my_rents


router = Router()
db_worker = DBWorkerAsync(engine_async)
bot = Bot(token=BOT_TOKEN)


class RentGroup(StatesGroup):
    waiting_to_gm = State()
    waiting_to_text = State()
    waiting_to_contact_link = State()


@router.callback_query(F.data == "add_rent_add")
async def add_rent_add(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        user_id_in_db = await db_worker.custom_orm_select(
            cls_from=Users.id,
            where_params=[Users.telegram_id == callback.message.chat.id],
        )
        user_id = user_id_in_db[0]

        sent_message = await callback.message.answer(
            text=(
                f"🧱 Введите кол-во гм для нового объявления целой цифрой, например "
                + "'9' или '15'. Обратите внимание, что вы можете указать 15 гм и указать "
                + "в описании, что это 2 дома 9гм "
                + "+ 6гм, при этом общее кол-во гм будет равно 15. После этого вы можете "
                + "отдельно создать два объявления для 9гм и 6гм, это немного увеличит "
                + "время создания, но упростит другам игрокам поиск гаражных мест."
            ),
        )
        await state.set_state(RentGroup.waiting_to_gm)
        await state.update_data(callback=callback)
        await state.update_data(gm_message_id=sent_message.message_id)
        await state.update_data(user_id=user_id)

    except Exception as exception:
        await sth_error(callback.message, exception)


@router.message(RentGroup.waiting_to_gm)
async def processing_gm(message: Message, state: FSMContext) -> None:
    try:
        new_gm = int(message.text)
        state_data = await state.get_data()
        callback: CallbackQuery = state_data["callback"]
        gm_message_id = state_data["gm_message_id"]
        if new_gm < 1 or new_gm > 36:
            await callback.message.delete()
            await message.delete()
            await bot.delete_message(chat_id=message.chat.id, message_id=gm_message_id)
            raise ValueError(
                "Кол-во гм, которое вы указали меньше 1 или больше 36, то есть выходит за допустимые лимиты"
            )

        sent_message = await message.answer(
            text=(
                f"📑 Укажите текст для вышего объявления, любые тонкости, а также "
                + "стоимость аренды стоит указать здесь, чтобы у арендатора было "
                + "полное представление о характере, оказываемой услуги"
            ),
        )
        await state.set_state(RentGroup.waiting_to_text)
        await state.update_data(user_gm_message_id=message.message_id)
        await state.update_data(text_message_id=sent_message.message_id)
        await state.update_data(new_gm=new_gm)

    except Exception as exception:
        await sth_error(message, exception)


@router.message(RentGroup.waiting_to_text)
async def processing_text(message: Message, state: FSMContext) -> None:
    try:
        new_text = message.text

        sent_message = await message.answer(
            text=(
                f"🪪 Укажите контактную ссылку, по которой можно с вами связаться в формате 'https://t.me/...' или 'https://vk.com/...'."
            ),
        )
        await state.set_state(RentGroup.waiting_to_contact_link)
        await state.update_data(user_text_message_id=message.message_id)
        await state.update_data(contact_link_message_id=sent_message.message_id)
        await state.update_data(new_text=new_text)

    except Exception as exception:
        await sth_error(message, exception)


@router.message(RentGroup.waiting_to_contact_link)
async def processing_text(message: Message, state: FSMContext) -> None:
    try:
        new_contact_link = message.text

        state_data = await state.get_data()
        callback: CallbackQuery = state_data["callback"]
        user_id = state_data["user_id"]

        gm_message_id = state_data["gm_message_id"]
        text_message_id = state_data["text_message_id"]
        contact_link_message_id = state_data["contact_link_message_id"]
        user_gm_message_id = state_data["user_gm_message_id"]
        user_text_message_id = state_data["user_text_message_id"]
        user_contact_link_message_id = message.message_id

        new_gm = state_data["new_gm"]
        new_text = state_data["new_text"]

        await bot.delete_message(chat_id=message.chat.id, message_id=gm_message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=text_message_id)
        await bot.delete_message(
            chat_id=message.chat.id, message_id=contact_link_message_id
        )
        await bot.delete_message(chat_id=message.chat.id, message_id=user_gm_message_id)
        await bot.delete_message(
            chat_id=message.chat.id, message_id=user_text_message_id
        )
        await bot.delete_message(
            chat_id=message.chat.id, message_id=user_contact_link_message_id
        )

        if (
            "https://t.me/" not in new_contact_link
            and "https://vk.com/" not in new_contact_link
        ):
            await bot.delete_message(
                chat_id=message.chat.id, message_id=callback.message.message_id
            )
            raise ValueError("упс... кажется вы указали некорректную ссылку")

        data_to_insert = {
            "user_id": user_id,
            "number_of_gm": new_gm,
            "add_text": new_text,
            "contact_link": new_contact_link,
            "created_at": datetime.utcnow(),
            "last_check": datetime.utcnow(),
        }
        await db_worker.custom_insert(cls_to=RentAdds, data=[data_to_insert])

        await my_rents(callback=callback)

    except Exception as exception:
        await sth_error(message, exception)


@router.callback_query(F.data.startswith("delete_rent_add"))
async def delete_rent_add(callback: CallbackQuery) -> None:
    try:
        rent_add_id = int(callback.data.split("|")[1])

        await db_worker.custom_orm_delete(
            cls_from=RentAdds, where_params=[RentAdds.id == rent_add_id]
        )

        await my_rents(callback=callback)

    except Exception as exception:
        await sth_error(callback.message, exception)
