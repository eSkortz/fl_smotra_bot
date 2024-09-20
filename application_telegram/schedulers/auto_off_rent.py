from datetime import datetime, timedelta

from config import database_engine_async, DAYS_FOR_OFF
from database.oop.database_worker_async import DatabaseWorkerAsync


database_worker = DatabaseWorkerAsync(database_engine_async)
target_date = datetime.utcnow() - timedelta(days=DAYS_FOR_OFF)


async def auto_off_rent_function() -> None: ...
