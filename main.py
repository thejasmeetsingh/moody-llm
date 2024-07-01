import uuid
import datetime
from typing import Annotated, Any

import redis.asyncio as redis
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, status

from schemas import UserID, UserMessage, SystemMessage, MessageHistory, Response
from llm import get_llm_response

app = FastAPI()
app.title = "Moody LLM"
app.description = "A LLM whose mood keeps changing."


async def get_redis():
    r = await redis.Redis(decode_responses=True)
    try:
        yield r
    except Exception as _:
        await r.close()


async def get_chat_history(_redis: redis.Redis, user_id: str) -> list:
    history = await _redis.get(str(user_id))
    if not history:
        history = []
    return history


@app.get(path="/api/user_id/", response_model=Response, status_code=status.HTTP_200_OK)
async def get_user_id():
    return Response(
        message="UserID generated successfully",
        data=UserID(user_id=uuid.uuid4())
    )


@app.get(path="/api/history/{user_id}/", response_model=Response, status_code=status.HTTP_200_OK)
async def get_chat_history(_redis: Annotated[redis.Redis, Depends(get_redis)], user_id: uuid.UUID):
    history: list = get_chat_history(_redis, str(user_id))
    response = []

    for _history in history:
        _user: dict[str, str] = _history["user"]
        _system: dict[str, str] = _history["system"]

        response.append(MessageHistory(
            user=UserMessage(
                message=_user["message"],
                timestamp=_user["timestamp"]
            ),
            system=SystemMessage(
                message=_system["message"],
                timestamp=_system["timestamp"],
                mood=_system["mood"]
            )
        ))

    return Response(message="Message History", data=response)


@app.websocket(path="/chat/{user_id}/")
async def chat(websocket: WebSocket, user_id: uuid.UUID, _redis: Annotated[redis.Redis, Depends(get_redis)]):
    await websocket.accept()
    try:
        while True:
            user_message: dict[str, Any] = await websocket.receive_json()

            if not user_message.get("message"):
                await websocket.send_denial_response()
                break

            user_message.update({
                "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
            })

            history: list = get_chat_history(_redis, str(user_id))

            system_message: dict[str, Any] = get_llm_response(history,
                                                              user_message["message"])

            system_message.update({
                "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
            })

            message = {
                "user": user_message,
                "system": system_message
            }

            history.append(message)
            _redis.set(str(user_id), history)

            await websocket.send_json(data=user_message)
    except WebSocketDisconnect:
        await websocket.close()
