import asyncio
from datetime import datetime
import io
import base64
import random

from config import database_engine_async
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_users_model import Users
from database.orm.public_users_pointers_model import UsersPointers
from database.orm.public_discord_adds_model import DiscordAdds
from database.orm.public_sent_discord_adds_model import SentDiscordAdds

from utils.discord_utils import post_with_images, post_without_images
from utils.text_utils import CHAPTER_CLASSIFICATION


database_worker = DatabaseWorkerAsync(database_engine_async)
local_semaphore = asyncio.Semaphore(20)


async def send_by_chapter(
    user_id: int, chapter_name: str, semaphore: asyncio.Semaphore
) -> None:
    async with semaphore:

        user: Users = await database_worker.custom_orm_select(
            cls_from=Users, where_params=[Users.id == user_id], get_unpacked=True
        )

        discord_add: DiscordAdds = await database_worker.custom_orm_select(
            cls_from=DiscordAdds,
            where_params=[
                DiscordAdds.user_id == user_id,
                DiscordAdds.chapter == chapter_name,
            ],
            get_unpacked=True,
        )

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

            timer_range = {
                range(60, 90): lambda: random.randint(60, 89),
                range(90, 120): lambda: random.randint(90, 119),
                range(120, 150): lambda: random.randint(120, 149),
                range(150, 180): lambda: random.randint(150, 179),
                range(180, 240): lambda: random.randint(180, 239),
                range(240, 480): lambda: random.randint(240, 479),
                range(480, 1001): lambda: random.randint(480, 1000),
            }
            for key, value in timer_range.items():
                if discord_add.timer in key:
                    new_timer = value()

            data_to_update = {"id": discord_add.id, "timer": new_timer}
            await database_worker.custom_orm_bulk_update(
                cls_to=DiscordAdds, data=[data_to_update]
            )

            data_to_insert = {
                "user_id": user.id,
                "message_id": response["id"],
                "channel_id": CHAPTER_CLASSIFICATION[chapter_name]["channel_id"],
            }
            await database_worker.custom_insert(
                cls_to=SentDiscordAdds, data=[data_to_insert]
            )


async def processing_chapter(chapter_name: str, pointer_model) -> None:
    data_by_pointer_in_db = await database_worker.custom_orm_select(
        cls_from=[UsersPointers.user_id, pointer_model]
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
