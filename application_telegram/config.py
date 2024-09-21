from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

import asyncio
import functools

from env_reader import app_config


TELEGRAM_TOKEN = app_config.TELEGRAM_TOKEN.get_secret_value()
ADMIN_DISCORD_TOKEN = app_config.ADMIN_DISCORD_TOKEN.get_secret_value()

DATABASE_LOGIN = app_config.DATABASE_LOGIN.get_secret_value()
DATABASE_PASSWORD = app_config.DATABASE_PASSWORD.get_secret_value()
DATABASE_IP = app_config.DATABASE_IP.get_secret_value()
DATABASE_NAME = app_config.DATABASE_NAME.get_secret_value()

DISCORD_CAPTION = ""
REACTIONS_LIST = ["pUwu%3A760501989532237844/%40me"]
SYMBOLS_BLACKLIST = ["#", "`", ">"]
DAYS_FOR_DELETE = 2
DAYS_FOR_OFF = 7
NON_PREMIUM_TIMER = 180
PREMIUM_TIMER = 60


database_engine = create_engine(
    f"postgresql+psycopg2://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@{DATABASE_IP}/{DATABASE_NAME}",
)
database_engine_async = create_async_engine(
    f"postgresql+asyncpg://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@{DATABASE_IP}/{DATABASE_NAME}",
)


def batch_lengh_generator(step: int, data: list) -> list:
    return (data[x : x + step] for x in range(0, len(data), step))


def equal_split(list_to_split, n_parts) -> tuple:
    k, m = divmod(len(list_to_split), n_parts)
    return (
        list_to_split[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)]
        for i in range(n_parts)
    )


def retry_async(num_attempts):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for try_index in range(num_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    print(
                        f"Exception occurred: {e}. Retrying... ({try_index}/{num_attempts})"
                    )
                    await asyncio.sleep(1)
            else:
                print(f"Failed after {num_attempts} attempts.")

        return wrapper

    return decorator
