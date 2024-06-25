from pydantic import BaseModel, UUID4, Field


class UserID(BaseModel):
    user_id: UUID4


class SocketMessage(BaseModel):
    message: str = Field(max_length=2000)


class Response(BaseModel):
    message: str
    data: SocketMessage | UserID
