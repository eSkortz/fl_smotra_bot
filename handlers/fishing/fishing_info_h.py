from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from config import engine_async
from db.oop.alchemy_di_async import DBWorkerAsync
from db.orm.schema_public import Fishing

from handlers.main_h import sth_error
from keyboards.fishing import only_to_fishing_k


router = Router()
db_worker = DBWorkerAsync(engine_async)


@router.callback_query(F.data.startswith("fish_info"))
async def fishing_info(callback: CallbackQuery) -> None:
    try:
        depth_tag = int(callback.data.split("|")[1])
        text = await db_worker.custom_orm_select(
            cls_from=Fishing.text, where_params=[Fishing.depth == depth_tag]
        )
        text = text[0]
        markup_inline = only_to_fishing_k.get()
        photo = FSInputFile("src/fishing.png")
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=photo, caption=text, reply_markup=markup_inline
        )
    except Exception as exception:
        await sth_error(callback.message, exception)
