from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from datetime import datetime

from config import engine_async, BOT_TOKEN
from db.oop.alchemy_di_async import DBWorkerAsync
from db.orm.schema_public import UserPointers, Users, DiscordAdds

from handlers.main_h import sth_error
from handlers.discord.my_add_menu_h import my_add_menu
from utils.text_utils import CHAPTER_CLASSIFICATION


router = Router()
db_worker = DBWorkerAsync(engine_async)
bot = Bot(token=BOT_TOKEN)


class AddsFunctions(StatesGroup):
    waiting_to_timer = State()


@router.callback_query(F.data.startswith("add_on_off"))
async def add_on_off(callback: CallbackQuery) -> None:
    try:
        chapter_name = callback.data.split("|")[1]
        pointer_model = CHAPTER_CLASSIFICATION[chapter_name]["pointer_model"]
        pointer_column_name = CHAPTER_CLASSIFICATION[chapter_name][
            "pointer_column_name"
        ]

        user_id = await db_worker.custom_orm_select(
            cls_from=Users.id,
            where_params=[Users.telegram_id == callback.message.chat.id],
        )
        user_id = user_id[0]

        pointer_in_db = await db_worker.custom_orm_select(
            cls_from=[UserPointers.id, pointer_model],
            where_params=[UserPointers.user_id == user_id],
        )
        pointer_id, pointer_value = pointer_in_db[0][0], pointer_in_db[0][1]

        data_to_update = {
            "id": pointer_id,
            pointer_column_name: False if pointer_value else True,
        }
        await db_worker.custom_orm_bulk_update(
            cls_to=UserPointers, data=[data_to_update]
        )

        await my_add_menu(callback=callback, chapter_name=chapter_name)

    except Exception as exception:
        await sth_error(callback.message, exception)


@router.callback_query(F.data.startswith("change_timer"))
async def change_timer(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        chapter_name = callback.data.split("|")[1]

        sent_message = await callback.message.answer(
            text=(
                "⏰ Введите значение таймера в минутах (например: 120, 240, 30). "
                + "Обратите внимание, что для пользователей, не обладающих "
                + "премиум-доступом, минимально-допустимое значение таймера 120. "
                + "в случае, если вы введете значение ниже допустимого порога, - "
                + "скрипт автоматически выставит минимально-возможное для вас значение"
            )
        )

        await state.set_state(AddsFunctions.waiting_to_timer)
        await state.update_data(chapter_name=chapter_name)
        await state.update_data(callback=callback)
        await state.update_data(id_to_delete=sent_message.message_id)

    except Exception as exception:
        await sth_error(callback.message, exception)


@router.message(AddsFunctions.waiting_to_timer)
async def processing_timer(message: Message, state: FSMContext) -> None:
    try:
        new_timer = int(message.text)
        state_data = await state.get_data()
        id_to_delete = int(state_data["id_to_delete"])
        chapter_name = state_data["chapter_name"]
        callback = state_data["callback"]

        await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
        await message.delete()

        user_in_db = await db_worker.custom_orm_select(
            cls_from=Users,
            where_params=[Users.telegram_id == message.chat.id],
        )
        user_in_db: Users = user_in_db[0]
        user_id, is_user_have_premium = user_in_db.id, user_in_db.is_have_premium

        add_in_db = await db_worker.custom_orm_select(
            cls_from=DiscordAdds,
            where_params=[
                DiscordAdds.user_id == user_id,
                DiscordAdds.chapter == chapter_name,
            ],
        )
        add_in_db: DiscordAdds = add_in_db[0]

        if new_timer < 30:
            new_timer = 30
        if new_timer < 120 and not is_user_have_premium:
            new_timer = 120

        data_to_update = {
            "id": add_in_db.id,
            "timer": new_timer,
            "updated_at": datetime.utcnow(),
        }
        await db_worker.custom_orm_bulk_update(
            cls_to=DiscordAdds, data=[data_to_update]
        )

        await my_add_menu(callback=callback, chapter_name=chapter_name)

    except Exception as exception:
        await sth_error(message, exception)
