import asyncio
import datetime
from servece.query import QUERY_ADD_MESSAGE, QUERY_UPDATE_MESSAGE
import asyncpg


async def create_pool():
    """Создает подключение к БД"""
    return await asyncpg.create_pool('postgresql://127.0.0.1:5432/postgres', min_size=1, max_size=80)


async def add_status_message(datetime_send_message: datetime.datetime, status_message: str,
                             id_mailing: int, id_client: int):
    '''Берет message по id'''
    db_pool = await create_pool()
    res = await db_pool.fetchrow(QUERY_ADD_MESSAGE, datetime_send_message, status_message, id_mailing,
                                 id_client)
    await db_pool.close()
    return res


async def update_status_message(id_message: int):
    """Обновляет статус сообщения на derived"""
    db_pool = await create_pool()
    await db_pool.fetchrow(QUERY_UPDATE_MESSAGE, id_message)
    await db_pool.close()


loop = asyncio.get_event_loop()
loop.create_task(create_pool())
