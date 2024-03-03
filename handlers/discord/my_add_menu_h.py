from aiogram import Router, F
from aiogram.types import CallbackQuery

from config import engine_async
from db.oop.alchemy_di_async import DBWorkerAsync
from db.orm.schema_public import Users, UserPointers, DiscordAdds

from handlers.main_h import sth_error
from keyboards.discord import my_add_menu_k
from utils.text_utils import CHAPTER_CLASSIFICATION, BOOL_TO_STATUS_ADDS
from utils.func_utils import combine_images


router = Router()
db_worker = DBWorkerAsync(engine_async)


@router.callback_query(F.data.startswith("discord_my_add"))
async def my_add_menu(callback: CallbackQuery, chapter_name: str = None) -> None:
    try:
        if not chapter_name:
            chapter_name = callback.data.split("|")[1]

        user_id = await db_worker.custom_orm_select(
            cls_from=Users.id,
            where_params=[Users.telegram_id == callback.message.chat.id],
        )
        user_id = user_id[0]

        pointer_model = CHAPTER_CLASSIFICATION[chapter_name]["pointer_model"]
        pointer_in_db = await db_worker.custom_orm_select(
            cls_from=pointer_model, where_params=[UserPointers.user_id == user_id]
        )
        pointer_value: bool = pointer_in_db[0]

        add_in_db = await db_worker.custom_orm_select(
            cls_from=DiscordAdds,
            where_params=[
                DiscordAdds.user_id == user_id,
                DiscordAdds.chapter == chapter_name,
            ],
        )
        add_in_db: DiscordAdds = add_in_db[0]

        markup_inline = my_add_menu_k.get(chapter_name)
        text = (
            f"Мое объявление в разделе {CHAPTER_CLASSIFICATION[chapter_name]['emoji']} "
            + f"{CHAPTER_CLASSIFICATION[chapter_name]['name']}\n\n"
            + f"🧭 Статус: {BOOL_TO_STATUS_ADDS[pointer_value]}\n"
            + f"⏰ Таймер: {add_in_db.timer} минут\n"
            + f"🎑 Кол-во фотографий: {len(add_in_db.images)}"
        )
        await callback.message.delete()

        if add_in_db.images:
            combine_photo = combine_images(add_in_db.images)
            await callback.message.answer_photo(
                photo=combine_photo, text=text, reply_markup=markup_inline
            )
        else:
            await callback.message.answer(
                text=text,
                reply_markup=markup_inline,
            )
    except Exception as exception:
        await sth_error(callback.message, exception)
