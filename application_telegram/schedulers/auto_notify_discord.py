from aiogram import Bot
from aiogram import types

import asyncio
from typing import List

from config import database_engine_async, ADMIN_DISCORD_TOKEN, TELEGRAM_TOKEN
from keyboards import link_and_main_k

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_users_model import Users
from database.orm.public_notifications_model import Notifications

from utils.discord_utils import get_messages
from utils.text_utils import CHAPTER_CLASSIFICATION


database_worker = DatabaseWorkerAsync(database_engine_async)
bot = Bot(token=TELEGRAM_TOKEN)


async def send_notify_to_user(
    user_id: int, tag: str, channel_id: str, message_id: str
) -> None:
    user: Users = await database_worker.custom_orm_select(
        cls_from=Users, where_params=[Users.id == user_id]
    )
    markup_inline = link_and_main_k.get(
        url=f"https://discord.com/channels/668553971618807818/{channel_id}/{message_id}"
    )
    text = f"🔔 По ключевому слову {tag} найдено новое упоминание"
    await bot.send_message(
        chat_id=user.telegram_id, text=text, reply_markup=markup_inline
    )


async def auto_notify_discord_function() -> None:
    notifications_list: List[Notifications] = await database_worker.custom_orm_select(
        cls_from=Notifications,
    )
    all_messages = []
    for value in CHAPTER_CLASSIFICATION.values():
        messages = await get_messages(
            authorization=ADMIN_DISCORD_TOKEN, channel_id=value["channel_id"]
        )
        all_messages = [*all_messages, *messages]

    task_list = []
    for notification_row in notifications_list:
        notification_row: Notifications
        for message in all_messages:
            if notification_row.tag in message["content"]:
                task_list.append(
                    asyncio.create_task(
                        send_notify_to_user(
                            user_id=notification_row.user_id,
                            tag=notification_row.tag,
                            channel_id=message["channel_id"],
                            message_id=["id"],
                        )
                    )
                )

    asyncio.gather(*task_list)
