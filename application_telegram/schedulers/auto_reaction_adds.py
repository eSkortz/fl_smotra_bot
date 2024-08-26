import asyncio

from config import database_engine_async, REACTIONS_LIST
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_users_model import Users
from database.orm.public_sent_discord_adds_model import SentDiscordAdds

from utils.discord_utils import put_reaction


database_worker = DatabaseWorkerAsync(database_engine_async)
local_semaphore = asyncio.Semaphore(20)


async def processing_symbol(
    tokens: list,
    message: SentDiscordAdds,
    reaction: str,
    semaphore: asyncio.Semaphore,
) -> None:
    async with semaphore:
        task_list = [
            asyncio.create_task(
                put_reaction(
                    authorization=token,
                    reaction=reaction,
                    channel_id=message.channel_id,
                    message_id=message.message_id,
                )
            )
            for token in tokens
        ]
        await asyncio.gather(*task_list)


async def auto_put_reactions_function() -> None:
    tokens = await database_worker.custom_orm_select(
        cls_from=Users.discord_token, where_params=[Users.discord_token != None]
    )
    messages = await database_worker.custom_orm_select(
        cls_from=SentDiscordAdds, where_params=[SentDiscordAdds.is_reaction == False]
    )

    for reaction in REACTIONS_LIST:
        tasks = [
            asyncio.create_task(
                processing_symbol(
                    tokens=tokens,
                    message=message,
                    reaction=reaction,
                    semaphore=local_semaphore,
                )
            )
            for message in messages
        ]
        await asyncio.gather(*tasks)

    data_to_update = []
    for message in messages:
        message: SentDiscordAdds
        message.is_reaction = True
        message_dict = message.__dict__
        del message_dict["_sa_instance_state"]
        data_to_update.append(message_dict)

    await database_worker.custom_orm_bulk_update(cls_to=SentDiscordAdds, data=data_to_update)
