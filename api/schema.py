from pydantic import BaseModel, Field
from datetime import datetime


class ResponseDeleteMailingSchema(BaseModel):
    id_mailing: int


class StaticCommonSchema(BaseModel):
    id_mailing: int
    count_message: int
    status: str


class StaticExactSchema(BaseModel):
    id_mailing: int
    id_message: int
    id_client: int
    send_datetime: datetime
    start_datetime_mailing: datetime
    end_datetime_mailing: datetime
    status: str
    text: str
    filter: str
    phone: str
    code_phone: str
    tag: str
    time_zone: str


class ResponseSchemaOk(BaseModel):
    status: str = 'ok'


class ResponseSchemaDelClient(BaseModel):
    id_client: int


class ResponseSchemaMailing(BaseModel):
    id_mailing: int


class ClientSchema(BaseModel):
    id_client: int
    phone: str
    code_phone: str
    tag: str
    time_zone: str


class MailingSchema(BaseModel):
    start_datetime: datetime = Field(...)
    text: str = Field(...)
    filter: str
    end_datetime: datetime = Field(...)


class ResponseMailingSchema(MailingSchema):
    id_mailing: int


class UpdateMailingSchema(BaseModel):
    start_datetime: datetime | None
    text: str | None
    filter: str | None
    end_datetime: datetime | None


class AddClientSchema(BaseModel):
    phone: str = Field(...)
    code_phone: str = Field(...)
    tag: str
    time_zone: str = Field(...)


class UpdateClientSchema(BaseModel):
    phone: str | None
    code_phone: str | None
    tag: str | None
    time_zone: str | None


class MessageSchema(BaseModel):
    send_datetime: datetime
    status: str
    id_mailing: int = Field(...)
    id_client: int = Field(...)


class ResponseClientSchema(AddClientSchema):
    id_client: int = Field(...)


class ErrorResponse(BaseModel):
    error: str
