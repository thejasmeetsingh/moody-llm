from pydantic import BaseModel, UUID4, Field


class UserID(BaseModel):
    user_id: UUID4


class UserMessage(BaseModel):
    content: str = Field(max_length=2000)
    timestamp: int


class AIMessage(BaseModel):
    content: str
    mood: int
    timestamp: int


class MessageHistory(BaseModel):
    message: UserMessage | AIMessage
    is_user: bool


class Response(BaseModel):
    message: str
    data: (
        UserID |
        UserMessage |
        AIMessage |
        list[MessageHistory]
    )
