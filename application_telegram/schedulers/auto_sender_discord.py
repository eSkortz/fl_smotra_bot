import asyncio
from datetime import datetime
import io
import base64

from config import engine_async
from db.oop.alchemy_di_async import DBWorkerAsync
from db.orm.schema_public import DiscordAdds, UserPointers, Users, SentDiscordAdds

from utils.discord_utils import post_with_images, post_without_images
from utils.text_utils import CHAPTER_CLASSIFICATION


db_worker = DBWorkerAsync(engine_async)
local_semaphore = asyncio.Semaphore(20)


async def send_by_chapter(
    user_id: int, chapter_name: str, semaphore: asyncio.Semaphore
) -> None:
    async with semaphore:

        user_in_db = await db_worker.custom_orm_select(
            cls_from=Users, where_params=[Users.id == user_id]
        )
        user: Users = user_in_db[0]

        discord_add_in_db = await db_worker.custom_orm_select(
            cls_from=DiscordAdds,
            where_params=[
                DiscordAdds.user_id == user_id,
                DiscordAdds.chapter == chapter_name,
            ],
        )
        discord_add: DiscordAdds = discord_add_in_db[0]

        time_difference = datetime.utcnow() - discord_add.last_sent
        time_difference = time_difference.total_seconds() // 60

        if time_difference > discord_add.timer:
            if discord_add.images:
                response = await post_with_images(
                    authorization=user.discord_token,
                    text=discord_add.text,
                    images=[
                        io.BufferedReader(io.BytesIO(base64.b64decode(base64_image)))
                        for base64_image in discord_add.images
                    ],
                    channel_id=CHAPTER_CLASSIFICATION[chapter_name]["channel_id"],
                )
            else:
                response = await post_without_images(
                    authorization=user.discord_token,
                    text=discord_add.text,
                    channel_id=CHAPTER_CLASSIFICATION[chapter_name]["channel_id"],
                )

            data_to_update = {"id": discord_add.id, "last_sent": datetime.utcnow()}
            await db_worker.custom_orm_bulk_update(
                cls_to=DiscordAdds, data=[data_to_update]
            )

            data_to_insert = {
                "user_id": user.id,
                "message_id": response["id"],
                "channel_id": CHAPTER_CLASSIFICATION[chapter_name]["channel_id"],
            }
            await db_worker.custom_insert(cls_to=SentDiscordAdds, data=[data_to_insert])


async def processing_chapter(chapter_name: str, pointer_model) -> None:
    data_by_pointer_in_db = await db_worker.custom_orm_select(
        cls_from=[UserPointers.user_id, pointer_model]
    )
    tasks_to_send = [
        asyncio.create_task(
            send_by_chapter(
                user_id=db_row[0], chapter_name=chapter_name, semaphore=local_semaphore
            )
        )
        for db_row in data_by_pointer_in_db
        if db_row[1]
    ]
    await asyncio.gather(*tasks_to_send)


async def auto_sender_discord_function() -> None:
    tasks = [
        asyncio.create_task(
            processing_chapter(chapter_name=key, pointer_model=values["pointer_model"])
        )
        for key, values in CHAPTER_CLASSIFICATION.items()
    ]
    await asyncio.gather(*tasks)
