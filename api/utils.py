import datetime
from api.query import (QUERY_ADD_CLIENT, QUERY_SELECT_CLIENT,
                       QUERY_UPDATE_CLIENT, QUERY_DELETE_CLIENT, QUERY_ADD_MAILING,
                       QUERY_GET_COMMON_STATISTIC, QUERY_GET_EXACT_STATISTIC, QUERY_SELECT_MAILING,
                       QUERY_UPDATE_MAILING, QUERY_DELETE_MAILING, QUERY_GET_MAILING_FROM_ID,
                       QUERY_GET_MAILING_FROM_FILTER)

import asyncpg


async def create_pool():
    """Создает подключение к БД"""
    return await asyncpg.create_pool('postgresql://127.0.0.1:5432/postgres', min_size=1, max_size=80)


async def client_add(client_phone: str, client_code_phone: str,
                     client_tag: str, client_time_zone: str):
    '''Добавляет клиента'''
    db_pool = await create_pool()
    await db_pool.fetch(QUERY_ADD_CLIENT, client_phone, client_code_phone,
                        client_tag, client_time_zone)
    await db_pool.close()


async def get_client(id_client: int):
    """Выбирает клиента по id"""
    db_pool = await create_pool()
    res = await db_pool.fetchrow(QUERY_SELECT_CLIENT, id_client)
    await db_pool.close()
    return res


async def update_client(id_client, phone, code_phone, tag, time_zone):
    """Обновляет клиента"""
    db_pool = await create_pool()
    res = await db_pool.fetchrow(QUERY_UPDATE_CLIENT, phone, code_phone, tag, time_zone, id_client)
    await db_pool.close()
    return res


async def client_delete(id_client):
    """ Удаляет клиента по id"""
    db_pool = await create_pool()
    res = await db_pool.fetchrow(QUERY_DELETE_CLIENT, id_client)
    await db_pool.close()
    return res


async def mailing_add(start_datetime, text, filter, end_datetime):
    """Добавляет рассылку"""
    db_pool = await create_pool()
    res = await db_pool.fetchrow(QUERY_ADD_MAILING, start_datetime, text, filter, end_datetime)
    await db_pool.close()
    return res


async def mailing_statistic_common():
    """Берет общую статистику по рассылкам"""
    db_pool = await create_pool()
    res = await db_pool.fetch(QUERY_GET_COMMON_STATISTIC)
    await db_pool.close()
    return res


async def mailing_statistic_exact(id_mailing: int):
    """Берет статистику по конкретной рассылке"""
    db_pool = await create_pool()
    res = await db_pool.fetch(QUERY_GET_EXACT_STATISTIC, id_mailing)
    await db_pool.close()
    return res


async def get_mailing(id_mailing: int):
    '''Берет рассылку по id'''
    db_pool = await create_pool()
    res = await db_pool.fetchrow(QUERY_SELECT_MAILING, id_mailing)
    await db_pool.close()
    if res is None:
        res = []
    return res


async def update_mailing(id_mailing: int, start_datetime: datetime.datetime, text: str, filter: str,
                         end_datetime: datetime.datetime):
    """Обновляет рассылку"""
    db_pool = await create_pool()
    await db_pool.fetchrow(QUERY_UPDATE_MAILING, start_datetime, text, filter, end_datetime, id_mailing)
    await db_pool.close()


async def mailing_delete(id_mailing: int):
    """ Удаляет рассылку по id"""
    db_pool = await create_pool()
    res = await db_pool.fetchrow(QUERY_DELETE_MAILING, id_mailing)
    await db_pool.close()
    return res


async def get_mailing_from_id(id_mailing: int):
    '''Берет рассылки по id'''
    db_pool = await create_pool()
    res = await db_pool.fetchrow(QUERY_GET_MAILING_FROM_ID, id_mailing)
    await db_pool.close()
    return res


async def get_client_from_filer(filter: str):
    '''Берет клиентов по фильтру'''
    db_pool = await create_pool()
    res = await db_pool.fetch(QUERY_GET_MAILING_FROM_FILTER, filter)
    await db_pool.close()
    return res


def set_id_mailing(list_mailing: list, id_mailing: int) -> list:
    """Выставляет id  текущей рассылки"""
    for mailing in list_mailing:
        mailing['id_mailing'] = id_mailing
    return list_mailing


def set_status_mailing(list_mailing: list) -> list:
    """Выставляет статус в not_send"""
    for mailing in list_mailing:
        mailing['status'] = 'not_send'
    return list_mailing
