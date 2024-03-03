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
    combined_image = Image.new(
        "RGB", (sum(img.width for img in images), max(img.height for img in images))
    )
    offset = 0
    for img in images:
        combined_image.paste(img, (offset, 0))
        offset += img.width
    photo_stream = io.BytesIO()
    combined_image.save(photo_stream, format="PNG")
    photo_stream.seek(0)
    return photo_stream
