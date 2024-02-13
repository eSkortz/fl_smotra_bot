from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from handlers.main_h import sth_error
from keyboards.fishing import only_to_fishing_k
from utils.text_utils import get_text_for_fishing

router = Router()


@router.callback_query(F.data.startswith("fish_info"))
async def fishing_info(callback: CallbackQuery) -> None:
    try:
        depth_tag = callback.data.split("|")[1]
        text = get_text_for_fishing(depth_tag=depth_tag)
        markup_inline = only_to_fishing_k.get()
        photo = FSInputFile("src/fishing.png")
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=photo, caption=text, reply_markup=markup_inline
        )
    except Exception as exception:
        await sth_error(callback.message, exception)
