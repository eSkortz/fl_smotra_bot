import asyncio
from datetime import datetime, timedelta

from config import database_engine_async, DAYS_FOR_DELETE
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_users_model import Users
from database.orm.public_sent_discord_adds_model import SentDiscordAdds

from utils.discord_utils import delete_message


database_worker = DatabaseWorkerAsync(database_engine_async)
local_semaphore = asyncio.Semaphore(20)
target_date = datetime.utcnow() - timedelta(days=DAYS_FOR_DELETE)


async def processing_task(
    authorization: str, channel_id: str, message_id: str, semaphore: asyncio.Semaphore
):
    async with semaphore:
        await delete_message(
            authorization=authorization, channel_id=channel_id, message_id=message_id
        )


async def auto_delete_discord_function() -> None:
    messages = await database_worker.custom_orm_select(
        cls_from=SentDiscordAdds,
        where_params=[
            SentDiscordAdds.is_deleted == False,
            SentDiscordAdds.sent_datetime <= target_date,
        ],
    )

    task_list = []
    data_to_update = []

    for message in messages:
        message: SentDiscordAdds

        message.is_deleted = True
        message_dict = message.__dict__
        del message_dict["_sa_instance_state"]
        data_to_update.append(message_dict)

        user_token = await database_worker.custom_orm_select(
            cls_from=Users.discord_token,
            where_params=[Users.id == SentDiscordAdds.user_id],
        )
        user_token = user_token[0]

        task = asyncio.create_task(
            processing_task(
                authorization=user_token,
                channel_id=message.channel_id,
                message_id=message.message_id,
                semaphore=local_semaphore,
            )
        )
        task_list.append(task)

    await asyncio.gather(*task_list)

    await database_worker.custom_orm_bulk_update(
        cls_to=SentDiscordAdds, data=data_to_update
    )
