import asyncio
from datetime import datetime, timedelta
from typing import List

from config import database_engine_async, DAYS_FOR_OFF
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_users_pointers_model import UsersPointers


database_worker = DatabaseWorkerAsync(database_engine_async)
target_date = datetime.utcnow() - timedelta(days=DAYS_FOR_OFF)


async def auto_off_adds_function() -> None:
    pointers_list: List[UsersPointers] = await database_worker.custom_orm_select(
        cls_from=UsersPointers, where_params=[UsersPointers.updated_at() < target_date]
    )
    data_to_update = []
    for pointer_row in pointers_list:
        pointer_row.business_pointer = False
        pointer_row.clothes_pointer = False
        pointer_row.global_pointer = False
        pointer_row.homes_pointer = False
        pointer_row.loot_pointer = False
        pointer_row.numbers_pointer = False
        pointer_row.services_pointer = False
        pointer_row.transport_pointer = False
        pointer_row.weapon_pointer = False
        temp_dict = pointer_row.__dict__
        del temp_dict["_sa_instance_state"]
        data_to_update.append(temp_dict)

    await database_worker.custom_orm_bulk_update(
        cls_to=UsersPointers, data=data_to_update
    )
