from aiogram import Router, F
from aiogram.types import CallbackQuery
from handlers.main_h import sth_error
from handlers.commands_h import fishing_command


router = Router()


@router.callback_query(F.data == "fishing_main")
async def fishing_main(callback: CallbackQuery) -> None:
    try:
        await callback.message.delete()
        await fishing_command(callback.message)
    except Exception as exception:
        await sth_error(callback.message, exception)
