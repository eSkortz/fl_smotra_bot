from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.main_h import sth_error
from keyboards.rent import my_rent_k

from config import engine_async
from db.oop.alchemy_di_async import DBWorkerAsync
from db.orm.schema_public import RentAdds, Users


router = Router()
db_worker = DBWorkerAsync(engine_async)


@router.callback_query(F.data == "my_rents")
async def my_rents(callback: CallbackQuery) -> None:
    try:
        user_id = await db_worker.custom_orm_select(
            cls_from=Users.id,
            where_params=[Users.telegram_id == callback.message.chat.id],
        )
        user_id = user_id[0]

        user_rent_adds = await db_worker.custom_orm_select(
            cls_from=RentAdds, where_params=[RentAdds.user_id == user_id]
        )
        markup_inline = my_rent_k.get(rent_adds_list=user_rent_adds)

        await callback.message.delete()
        await callback.message.answer(
            text="🏘 Мои объявления (ГМ). Здесь вы видите список всех размещенных вами объявлений",
            reply_markup=markup_inline,
        )
    except Exception as exception:
        await sth_error(callback.message, exception)
