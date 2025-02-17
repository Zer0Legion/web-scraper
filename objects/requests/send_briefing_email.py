from openai import BaseModel

from objects.requests.stock import StockRequestInfo


class SendEmailUserRequest(BaseModel):
    email: str
    name: str
    stocks: list[StockRequestInfo]


class SendEmailRequest(BaseModel):
    user_requests: list[SendEmailUserRequest]
