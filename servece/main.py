import datetime
import json
import aiohttp
import async_timeout
import asyncpg

from servece.utils import add_status_message, update_status_message

LOCAL_TZ = datetime.datetime.now().astimezone().tzinfo


async def fetch(session, url, headers=None, data=None):
    """Авторизация  JWT"""
    async with async_timeout.timeout(10):
        async with session.post(url, headers=headers, data=data) as response:
            return response


async def mailer(list_mailing: list):
    """Выполняет рассылку. Сообщения, которые вернули статус 200, записывают статус derived"""
    list_data = []
    for mailing in list_mailing:
        status_message = mailing.get('status')
        if status_message != 'derived':
            data = {
                "phone": int(mailing.get('phone').isdecimal()),
                "text": mailing.get('text')}
            datetime_send_message = datetime.datetime.now()
            id_mailing = int(mailing.get('id_mailing'))
            id_client = int(mailing.get('id_client'))
            try:
                msg_id = await add_status_message(datetime_send_message, status_message, id_mailing, id_client)
            except asyncpg.exceptions.ForeignKeyViolationError:
                return
            msg_id = int(msg_id['id_message'])
            data['id'] = msg_id
            data = json.dumps(data)
            list_data.append(data)
    for data in list_data:
        msg_id = json.loads(data)
        msg_id = msg_id['id']
        async with aiohttp.ClientSession() as session:
            response = await fetch(session, f'https://probe.fbrq.cloud/v1/send/{msg_id}',
                                   headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                                                             'eyJleHAiOjE2ODEzOTQyNjgsImlzcyI6ImZhYnJpcXVlI'
                                                             'iwibmFtZSI6IkRtaXRyaXlNIn0.615sRl_LUDFU9n7ublz'
                                                             'Cc3Iju8p6nqF-HtZ3ENvgUm4'}, data=data)
            if response.status == 200:
                print(msg_id)
                await update_status_message(msg_id)
