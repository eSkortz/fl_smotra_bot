from aiogram import Bot, Dispatcher

import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN

from schedulers.auto_sender_discord import auto_sender_discord_function


from handlers import commands_h, main_h, premium_h, support_h
from handlers.cars import cars_main_h, car_marks_h, car_info_h
from handlers.discord import (
    discord_h,
    my_adds_h,
    my_add_menu_h,
    adds_function_h,
    change_authorization_h,
    notifications_h,
)
from handlers.fishing import fishing_h, fishing_info_h
from handlers.rent import (
    rent_add_functions_h,
    rent_h,
    my_rents_h,
    my_rent_info_h,
    find_rent_h,
)


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()


async def main() -> None:
    scheduler.add_job(auto_sender_discord_function, trigger='interval', seconds=60)
    dp.include_routers(
        commands_h.router,
        main_h.router,
        premium_h.router,
        support_h.router,
        cars_main_h.router,
        discord_h.router,
        fishing_h.router,
        rent_h.router,
        my_adds_h.router,
        car_marks_h.router,
        car_info_h.router,
        fishing_info_h.router,
        my_add_menu_h.router,
        adds_function_h.router,
        change_authorization_h.router,
        notifications_h.router,
        my_rents_h.router,
        rent_add_functions_h.router,
        my_rent_info_h.router,
        find_rent_h.router,
    )
    await bot.delete_webhook(drop_pending_updates=True)

    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
