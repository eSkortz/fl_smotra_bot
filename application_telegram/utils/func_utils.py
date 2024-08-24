from aiogram.types import Message

import io
import base64
from PIL import Image

from db.oop.alchemy_di_async import DBWorkerAsync
from db.orm.schema_public import Users, UserPointers, DiscordAdds
from config import engine_async

from utils.text_utils import CHAPTER_CLASSIFICATION


db_worker = DBWorkerAsync(engine_async)


async def auto_registration(message: Message) -> None:
    user_in_db = await db_worker.custom_orm_select(
        cls_from=Users, where_params=[Users.telegram_id == message.chat.id]
    )

    if user_in_db == []:
        data_user = {
            "telegram_id": message.chat.id,
            "telegram_name": message.chat.username,
        }
        await db_worker.custom_insert(cls_to=Users, data=[data_user])

        user_in_db = await db_worker.custom_orm_select(
            cls_from=Users, where_params=[Users.telegram_id == message.chat.id]
        )
        user_in_db: Users = user_in_db[0]

        data_pointers = {
            "user_id": user_in_db.id,
        }
        await db_worker.custom_insert(cls_to=UserPointers, data=[data_pointers])

        chapter_names = [key for key in CHAPTER_CLASSIFICATION.keys()]

        adds_data = [
            {
                "user_id": user_in_db.id,
                "chapter": chapter_name,
            }
            for chapter_name in chapter_names
        ]
        await db_worker.custom_insert(cls_to=DiscordAdds, data=adds_data)


def combine_images(images_list: list) -> io.BytesIO:
    images = [Image.open(io.BytesIO(base64.b64decode(img))) for img in images_list]

    max_height = max(img.height for img in images)

    num_images = len(images)
    num_rows = (num_images + 4) // 5
    target_width = (
        max(
            sum(img.width for img in images[:5]), sum(img.width for img in images[5:-1])
        )
        if num_images > 5
        else sum(img.width for img in images)
    )
    target_height = max_height * num_rows

    combined_image = Image.new("RGB", (target_width, target_height))

    offset_x = 0
    offset_y = 0
    row_count = 0
    for i, img in enumerate(images):
        combined_image.paste(img, (offset_x, offset_y))
        offset_x += img.width
        row_count += 1
        if row_count == 5:
            offset_x = 0
            offset_y += max_height
            row_count = 0

    photo_stream = io.BytesIO()
    combined_image.save(photo_stream, format="PNG")
    photo_stream.seek(0)
    return photo_stream
