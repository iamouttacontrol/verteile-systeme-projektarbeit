from pydantic import BaseModel


class Message(BaseModel):
    name: str
    message: str
    language: str
    timestamp: str
    sentiment: float