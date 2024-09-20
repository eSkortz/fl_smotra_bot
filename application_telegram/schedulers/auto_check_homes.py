from aiogram import Bot
import asyncio
from typing import List

from config import database_engine_async, BOT_TOKEN

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_homes_model import Homes
from database.orm.public_users_model import Users


database_worker = DatabaseWorkerAsync(database_engine_async)
bot = Bot(BOT_TOKEN)


async def notify_user(home: Homes) -> None:
    user: Users = await database_worker.custom_orm_select(
        cls_from=Users, where_params=[Users.id == home.user_id], get_unpacked=True
    )
    await bot.send_message(
        chat_id=user.telegram_id,
        text=f"❗️ Ваш дом {home.name} дошел до баланса {home.balance}",
    )


async def auto_check_homes_function() -> None:
    homes_list: List[Homes] = await database_worker.custom_orm_select(cls_from=Homes)
    data_to_update = [
        {"id": home.id, "balance": home.balance - home.expenses} for home in homes_list
    ]
    await database_worker.custom_orm_bulk_update(cls_to=Homes, data=data_to_update)

    task_list = []
    homes_over_400: List[Homes] = await database_worker.custom_orm_select(
        cls_from=Homes, where_params=[Homes.balance >= 400, Homes.balance < 450]
    )
    for home in homes_over_400:
        task_list.append(asyncio.create_task(notify_user(home=home)))
    homes_over_450: List[Homes] = await database_worker.custom_orm_select(
        cls_from=Homes, where_params=[Homes.balance >= 450, Homes.balance < 500]
    )
    for home in homes_over_450:
        for _ in range(5):
            task_list.append(asyncio.create_task(notify_user(home=home)))

    await asyncio.gather(*task_list)
