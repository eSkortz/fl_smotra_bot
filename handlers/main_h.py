from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from keyboards import start_k, only_to_main_k
from handlers.commands_h import start_command
from config import BOT_TOKEN

router = Router()
bot = Bot(token=BOT_TOKEN)


class Patterns(StatesGroup):
    waiting_to_id = State()


async def sth_error(message: Message, error_text: str) -> None:
    markup_inline = only_to_main_k.get()
    await message.answer(
        text=f"⛔️ Что-то пошло не так\n\nТекст ошибки: {error_text}",
        reply_markup=markup_inline,
    )


@router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery) -> None:
    await callback.message.delete()
    await start_command(callback.message)
