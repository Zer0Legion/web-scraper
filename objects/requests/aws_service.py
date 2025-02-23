from openai import BaseModel
from pydantic import ConfigDict


class UploadImageRequest(BaseModel):

    file_path: str
    bucket: str