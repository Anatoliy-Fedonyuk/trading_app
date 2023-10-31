from pydantic import BaseModel


class MessagesModel(BaseModel):
    id: int
    messages: str

    class Config:
        orm_mode = True
