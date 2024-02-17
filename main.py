import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import commands_h, main_h, premium_h, support_h
from handlers.cars import cars_main_h, car_marks_h, car_info_h
from handlers.discord import discord_h, my_adds_h, my_add_menu_h
from handlers.fishing import fishing_h, fishing_info_h
from handlers.rent import rent_h
from handlers.loot import loot_h


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main() -> None:
    dp.include_routers(
        commands_h.router,
        main_h.router,
        premium_h.router,
        support_h.router,
        cars_main_h.router,
        discord_h.router,
        fishing_h.router,
        rent_h.router,
        loot_h.router,
        my_adds_h.router,
        car_marks_h.router,
        car_info_h.router,
        fishing_info_h.router,
        my_add_menu_h.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.create_task(dp.start_polling(bot))


if __name__ == "__main__":
    asyncio.run(main())
