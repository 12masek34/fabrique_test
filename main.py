import asyncio
import datetime
from fastapi import FastAPI, HTTPException
from api.schema import (AddClientSchema, ResponseClientSchema, UpdateClientSchema, MailingSchema,
                        UpdateMailingSchema, ResponseSchemaOk, ClientSchema,
                        ResponseSchemaMailing, ResponseSchemaDelClient, StaticCommonSchema, StaticExactSchema,
                        ResponseMailingSchema, ResponseDeleteMailingSchema)
from api.utils import (client_add, get_client, update_client, client_delete, mailing_add, mailing_statistic_common,
                       mailing_statistic_exact, get_mailing, update_mailing, mailing_delete, get_mailing_from_id,
                       get_client_from_filer, set_id_mailing, set_status_mailing)
from servece.main import mailer
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler

sched = AsyncIOScheduler(daemon=True)

LOCAL_TZ = datetime.datetime.now().astimezone().tzinfo

app = FastAPI()

sched.start()


@app.post('/client/add', status_code=201, response_model=ResponseSchemaOk)
async def post_client(client: AddClientSchema):
    await client_add(client.phone, client.code_phone,
                     client.tag, client.time_zone)
    return {'status': 'ok'}


@app.patch('/client/update/{id_client}', status_code=200, response_model=ClientSchema)
async def patch_client(id_client: int, client: UpdateClientSchema):
    stored_client = await get_client(id_client)
    if stored_client is None:
        raise HTTPException(status_code=404, detail='Client not found')
    stored_client = dict(stored_client)
    stored_client_model = ResponseClientSchema(**stored_client)
    update_data = client.dict(exclude_unset=True)
    client_update = stored_client_model.copy(update=update_data)
    res = await update_client(client_update.id_client, client_update.phone, client_update.code_phone,
                              client_update.tag, client_update.time_zone)
    return res


@app.delete('/client/delete/{id_client}', status_code=200, response_model=ResponseSchemaDelClient)
async def delete_client(id_client: int):
    res = await client_delete(id_client)
    if res is None:
        raise HTTPException(status_code=404, detail='Client not found')
    return res


@app.post('/mailing/add', status_code=201, response_model=ResponseSchemaMailing)
async def post_mailing(mailing: MailingSchema):
    id_mailing = dict(await mailing_add(mailing.start_datetime, mailing.text, mailing.filter, mailing.end_datetime))
    res = id_mailing
    id_mailing = int(id_mailing.get('id_mailing'))
    new_mailing = dict(await get_mailing_from_id(id_mailing))
    filter_mailing = new_mailing.get('filter')
    end_datetime = new_mailing.get('end_datetime')
    start_datetime = new_mailing.get('start_datetime')
    end_datetime = end_datetime.replace(tzinfo=LOCAL_TZ)
    start_datetime = start_datetime.replace(tzinfo=LOCAL_TZ)
    now_datetime = datetime.datetime.now(tz=LOCAL_TZ)
    list_mailing = await get_client_from_filer(filter_mailing)
    list_mailing = [dict(mailing) for mailing in list_mailing]
    list_mailing = set_id_mailing(list_mailing, id_mailing)
    list_mailing = set_status_mailing(list_mailing)
    if len(list_mailing) == 0:
        raise HTTPException(status_code=404, detail='No matches by filter')
    elif start_datetime < now_datetime < end_datetime:
        print('Рассылка началась')
        sched.add_job(mailer, 'date', run_date=datetime.datetime.now(), args=[list_mailing])
        return res
    elif now_datetime < start_datetime < end_datetime:
        print('Отложенная рассылка')
        sched.add_job(mailer, 'date', run_date=start_datetime, args=[list_mailing])
        return res
    elif end_datetime < now_datetime:
        print('Рассылка просрочена')
        raise HTTPException(status_code=422, detail='Overdue mailing')


@app.get('/statistic/common', status_code=200, response_model=list[StaticCommonSchema])
async def get_common_statistic_mailing():
    return await mailing_statistic_common()


@app.get('/statistic/exact', status_code=200, response_model=list[StaticExactSchema])
async def get_exact_statistic_mailing(id_mailing: int):
    res = await mailing_statistic_exact(id_mailing)
    if len(res) == 0:
        raise HTTPException(status_code=404, detail='Mailing not found')
    return res


@app.patch('/mailing/update/{id_mailing}', status_code=200, response_model=ResponseMailingSchema)
async def patch_mailing(id_mailing: int, mailing: UpdateMailingSchema):
    stored_mailing = dict(await get_mailing(id_mailing))
    if len(stored_mailing) == 0:
        raise HTTPException(status_code=404, detail='Mailing not found')
    stored_mailing_model = ResponseMailingSchema(**stored_mailing)
    update_data = mailing.dict(exclude_unset=True)
    mailing_update = stored_mailing_model.copy(update=update_data)
    await update_mailing(mailing_update.id_mailing, mailing_update.start_datetime, mailing_update.text,
                         mailing_update.filter, mailing_update.end_datetime)
    return mailing_update


@app.delete('/mailing/delete/{id_mailing}', status_code=200, response_model=ResponseDeleteMailingSchema)
async def delete_mailing(id_mailing: int):
    res = await mailing_delete(id_mailing)
    if res is None:
        raise HTTPException(status_code=404, detail='Mailing not found')
    return res


if __name__ == "__main__":
    asyncio.run(mailer())
    uvicorn.run(app, port=8000)
