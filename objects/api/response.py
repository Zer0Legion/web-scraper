from pydantic import BaseModel


class SuccessResponse(BaseModel):
    data: str


class ErrorResponse(BaseModel):
    error_code: int
    error_message: str
