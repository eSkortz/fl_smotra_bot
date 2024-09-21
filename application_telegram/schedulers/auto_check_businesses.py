from aiogram import Bot
import asyncio
from typing import List

from config import database_engine_async, TELEGRAM_TOKEN

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_businesses_model import Businesses
from database.orm.public_users_model import Users


database_worker = DatabaseWorkerAsync(database_engine_async)
bot = Bot(TELEGRAM_TOKEN)


async def notify_user(business: Businesses) -> None:
    user: Users = await database_worker.custom_orm_select(
        cls_from=Users, where_params=[Users.id == business.user_id], get_unpacked=True
    )
    await bot.send_message(
        chat_id=user.telegram_id,
        text=f"❗️ Ваш бизнес {business.name} дошел до кол-ва задач {business.tasks_count}",
    )


async def auto_check_businesses_function() -> None:
    business_list: List[Businesses] = await database_worker.custom_orm_select(
        cls_from=Businesses
    )
    data_to_update = [
        {"id": business.id, "balance": business.tasks_count + 1}
        for business in business_list
    ]
    await database_worker.custom_orm_bulk_update(cls_to=Businesses, data=data_to_update)

    task_list = []
    business_list: List[Businesses] = await database_worker.custom_orm_select(
        cls_from=Businesses,
        where_params=[Businesses.tasks_count == 4],
    )
    business_blacklist: List[Businesses] = await database_worker.custom_orm_select(
        cls_from=Businesses,
        where_params=[
            Businesses.tasks_count == 7,
            Businesses.tasks_count == 8,
        ],
    )
    for business in business_list:
        task_list.append(asyncio.create_task(notify_user(business=business)))
    for business in business_blacklist:
        for _ in range(5):
            task_list.append(asyncio.create_task(notify_user(business=business)))

    await asyncio.gather(*task_list)
