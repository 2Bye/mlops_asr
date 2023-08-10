from pydantic import BaseModel


class AudioDataModel(BaseModel):
    audio: str
    request_id: int = 1 


class Response(BaseModel):
    event: str
    text: str
    request_id: int = 1
