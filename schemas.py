from pydantic import BaseModel, UUID4, Field


class UserID(BaseModel):
    user_id: UUID4


class UserMessage(BaseModel):
    message: str = Field(max_length=2000)
    timestamp: str


class SystemMessage(BaseModel):
    message: str
    mood: int
    timestamp: str


class MessageHistory(BaseModel):
    user: UserMessage
    system: SystemMessage


class Response(BaseModel):
    message: str
    data: (
        UserID |
        UserMessage |
        SystemMessage |
        list[MessageHistory]
    )
