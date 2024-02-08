from pydantic import BaseModel


class MessageFromClient(BaseModel):
    username: str
    message: str
    language: str
    timestamp: str


class MessageToClient(BaseModel):
    username: str
    message: str
    language: str
    timestamp: str
    sentiment: float