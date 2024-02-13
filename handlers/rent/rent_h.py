from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from handlers.main_h import sth_error
from handlers.commands_h import rent_command
from config import BOT_TOKEN

router = Router()
bot = Bot(token=BOT_TOKEN)


@router.callback_query(F.data == "rent_main")
async def rent_main(callback: CallbackQuery) -> None:
    try:
        await callback.message.delete()
        await rent_command(callback.message)
    except Exception as exception:
        await sth_error(callback.message, exception)