from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums.parse_mode import ParseMode

from handlers.main_h import sth_error
from keyboards.fractions import only_to_fractions_k


router = Router()


@router.callback_query(F.data == "business_menu")
async def family_menu(callback: CallbackQuery) -> None:
    try:
        text = (
            ">🍺 Это раздел __*Семья*__, пока что сюда нечего добавить, но вскоре после обновления "
            "с контентом для семей здесь может что\-то появиться\."
        )
        markup_inline = only_to_fractions_k.get()
        await callback.message.delete()
        await callback.message.answer(
            text=text, reply_markup=markup_inline, parse_mode=ParseMode.MARKDOWN_V2
        )
    except Exception as exception:
        await sth_error(callback.message, exception)