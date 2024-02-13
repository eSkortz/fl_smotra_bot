from aiogram.types import Message

import datetime

from db.oop.alchemy_di_async import DBWorkerAsync
from db.orm.schema_public import (
    Users,
    UserPointers,
    TransportAdds,
    NumbersAdds,
    HomesAdds,
    BusinessAdds,
    LootAdds,
    WeaponAdds,
    ClothesAdds,
    ServicesAdds,
    GlobalAdds,
)
from config import engine_async


db_worker = DBWorkerAsync(engine_async)


async def auto_registration(message: Message) -> None:
    user_in_db = await db_worker.custom_orm_select(
        cls_from=Users, where_params=[Users.telegram_id == message.chat.id]
    )

    if user_in_db == []:
        data_user = {
            "telegram_id": message.chat.id,
            "telegram_name": message.chat.username,
            "discord_token": "",
            "is_have_premium": False,
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow(),
        }
        await db_worker.custom_insert(cls_to=Users, data=[data_user])

        user_in_db = await db_worker.custom_orm_select(
            cls_from=Users, where_params=[Users.telegram_id == message.chat.id]
        )
        user_in_db: Users = user_in_db[0]

        data_pointers = {
            "user_id": user_in_db.id,
            "transport_pointer": False,
            "numbers_pointer": False,
            "homes_pointer": False,
            "business_pointer": False,
            "clothes_pointer": False,
            "weapon_pointer": False,
            "loot_pointer": False,
            "services_pointer": False,
            "global_pointer": False,
        }
        await db_worker.custom_insert(cls_to=UserPointers, data=[data_pointers])

        adds_data = {
            "user_id": user_in_db.id,
            "text": "",
            "images": [],
            "timer": 120,
            "created_at": datetime.datetime.utcnow(),
            "last_sent": datetime.datetime.utcnow(),
        }
        await db_worker.custom_insert(cls_to=TransportAdds, data=[adds_data])
        await db_worker.custom_insert(cls_to=NumbersAdds, data=[adds_data])
        await db_worker.custom_insert(cls_to=HomesAdds, data=[adds_data])
        await db_worker.custom_insert(cls_to=BusinessAdds, data=[adds_data])
        await db_worker.custom_insert(cls_to=ClothesAdds, data=[adds_data])
        await db_worker.custom_insert(cls_to=WeaponAdds, data=[adds_data])
        await db_worker.custom_insert(cls_to=LootAdds, data=[adds_data])
        await db_worker.custom_insert(cls_to=ServicesAdds, data=[adds_data])
        await db_worker.custom_insert(cls_to=GlobalAdds, data=[adds_data])
