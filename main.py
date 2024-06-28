import uuid
from typing import Annotated

import redis.asyncio as redis
from fastapi import FastAPI, Depends, status

from schemas import UserID, UserMessage, SystemMessage, MessageHistory, Response

app = FastAPI()
app.title = "Moody LLM"
app.description = "A LLM whose mood keeps changing."


async def get_redis():
    r = await redis.Redis(decode_responses=True)
    try:
        yield r
    except Exception as _:
        await r.close()


@app.get(path="/api/user_id", response_model=Response, status_code=status.HTTP_200_OK)
async def get_user_id():
    return Response(
        message="UserID generated successfully",
        data=UserID(user_id=uuid.uuid4())
    )


@app.get(path="/api/history/{user_id}", response_model=Response, status_code=status.HTTP_200_OK)
async def get_chat_history(_redis: Annotated[redis.Redis, Depends(get_redis)], user_id: uuid.UUID):
    history: list[dict[str, dict[str, str]]] | None = await _redis.get(user_id)

    if not history:
        history = []

    response = []

    for _history in history:
        response.append(MessageHistory(
            user=UserMessage(
                message=_history["user"]["message"],
                timestamp=_history["user"]["timestamp"]
            ),
            system=SystemMessage(
                message=_history["system"]["message"],
                timestamp=_history["system"]["timestamp"],
                mood=_history["system"]["mood"]
            )
        ))

    return Response(message="Message History", data=response)
