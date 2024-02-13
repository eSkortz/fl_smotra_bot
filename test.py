from config import engine_async
from db.orm.schema_public import Cars
from db.oop.alchemy_di_async import DBWorkerAsync
import asyncio
from sqlalchemy import and_, or_


db_worker = DBWorkerAsync(engine_async)


async def get_users() -> None:
    cars = await db_worker.custom_orm_select(
        cls_from=Cars,
        where_params=[
            and_(
                Cars.classification.like("%elite%"),
                Cars.name.like('%bugatti%'),
                or_(Cars.id == 1, Cars.max_speed > 270),
            )
        ],
    )
    for car in cars:
        car: Cars


# async def get_users_native() -> None:
#     from config import engine_async
#     from sqlalchemy.ext.asyncio import async_sessionmaker
#     from sqlalchemy import select
#     from db.orm.schema_public import Users

#     async_session = async_sessionmaker(engine_async, expire_on_commit=True)

#     async with async_session() as session:
#         stmt = select(Users)
#         users = await session.scalars(stmt)
#         result = users.all()
#         for user in result:
#             user: Users
#             print(user.telegram_id)


# async def insert_user_native() -> None:
#     from config import engine_async
#     from sqlalchemy.ext.asyncio import async_sessionmaker
#     from sqlalchemy import select, insert
#     from db.orm.schema_public import Users

#     data = {
#         "telegram_id": 1,
#         "telegram_name": "test",
#         "discord_token": "",
#         "is_have_premium": False,
#     }

#     async_session = async_sessionmaker(engine_async, expire_on_commit=True)

#     async with async_session() as session:
#         stmt = insert(Users)
#         await session.execute(stmt, data)
#         await session.commit()

#     await get_users()


asyncio.run(get_users())
