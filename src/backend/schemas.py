from pydantic import BaseModel, UUID4, Field


class UserID(BaseModel):
    user_id: UUID4


class UserMessage(BaseModel):
    message: str = Field(max_length=2000)
    timestamp: str


class AIMessage(BaseModel):
    message: str
    mood: int
    timestamp: str


class MessageHistory(BaseModel):
    user: UserMessage
    ai: AIMessage


class Response(BaseModel):
    message: str
    data: (
        UserID |
        UserMessage |
        AIMessage |
        list[MessageHistory]
    )
