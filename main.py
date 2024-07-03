import os
import uuid
import datetime
from typing import Annotated, Any

from dotenv import load_dotenv
from supabase import AClient
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, status

from schemas import UserID, UserMessage, SystemMessage, MessageHistory, Response
from storage import get_client, get_messages, add_message
from llm import get_llm_response


load_dotenv()

app = FastAPI()
app.title = "Moody LLM"
app.description = "A LLM whose mood keeps changing."


@app.get(path="/api/user_id/", response_model=Response, status_code=status.HTTP_200_OK)
async def get_user_id():
    return Response(
        message="UserID generated successfully",
        data=UserID(user_id=uuid.uuid4())
    )


@app.get(path="/api/history/{user_id}/", response_model=Response, status_code=status.HTTP_200_OK)
async def get_user_chat_history(client: Annotated[AClient, Depends(get_client)], user_id: uuid.UUID):
    history: list = await get_messages(client, user_id)
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
async def chat(websocket: WebSocket, user_id: uuid.UUID, client: Annotated[AClient, Depends(get_client)]):
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

            history: list = await get_messages(client, user_id, limit=25)

            system_message: dict[str, Any] = await get_llm_response(history,
                                                                    user_message["message"])

            system_message.update({
                "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
            })

            message = {
                "user": user_message,
                "system": system_message
            }

            await add_message(client, user_id, message)
            await websocket.send_json(data=system_message)
    except WebSocketDisconnect:
        await websocket.close()
