from aiogram import Router, F
from aiogram.types import CallbackQuery

from config import engine_async
from db.oop.alchemy_di_async import DBWorkerAsync
from db.orm.schema_public import Users, UserPointers
from handlers.main_h import sth_error
from keyboards.discord import my_add_menu_k
from utils.text_utils import CHAPTER_CLASSIFICATION, pointer_by_chapter_name


router = Router()
db_worker = DBWorkerAsync(engine_async)


@router.callback_query(F.data.startswith("discord_my_add"))
async def my_add_menu(callback: CallbackQuery) -> None:
    try:
        chapter_name = callback.data.split("|")[1]

        user_id = await db_worker.custom_orm_select(
            cls_from=Users.id,
            where_params=[Users.telegram_id == callback.message.chat.id],
        )
        user_id = user_id[0]
        user_pointers = await db_worker.custom_orm_select(
            cls_from=UserPointers, where_params=[UserPointers.user_id == user_id]
        )
        user_pointers: UserPointers = user_pointers[0]

        markup_inline = my_add_menu_k.get(chapter_name)
        await callback.message.delete()
        await callback.message.answer(
            text=(
                f"Мое объявление в разделе {CHAPTER_CLASSIFICATION[chapter_name]['emoji']} "
                + f"{CHAPTER_CLASSIFICATION[chapter_name]['name']} \n"
                + f"({pointer_by_chapter_name(pointers_model=user_pointers, chapter_name=chapter_name)})"
            ),
            reply_markup=markup_inline,
        )
    except Exception as exception:
        await sth_error(callback.message, exception)
