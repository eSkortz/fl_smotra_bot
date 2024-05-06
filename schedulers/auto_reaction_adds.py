import asyncio

from config import engine_async, REACTIONS_LIST
from db.oop.alchemy_di_async import DBWorkerAsync
from db.orm.schema_public import Users, SentDiscordAdds

from utils.discord_utils import put_reaction


db_worker = DBWorkerAsync(engine_async)
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
    tokens = await db_worker.custom_orm_select(
        cls_from=Users.discord_token, where_params=[Users.discord_token != None]
    )
    messages = await db_worker.custom_orm_select(
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

    await db_worker.custom_orm_bulk_update(cls_to=SentDiscordAdds, data=data_to_update)
