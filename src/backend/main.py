import uuid
import datetime
from typing import Annotated, Any

from dotenv import dotenv_values
from supabase import acreate_client
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, status

from storage import Storage, StorageException
from llm import get_llm_response
from schemas import UserID, Response, UserMessage, AIMessage, MessageHistory

app = FastAPI()
app.title = "Moody LLM"
app.description = "A LLM whose mood keeps changing."


async def get_storage():
    config = dotenv_values()

    table = config.get("SUPABASE_TABLE_NAME")
    url = config.get("SUPABASE_URL")
    key = config.get("SUPABASE_KEY")

    if not table or not url or not key:
        raise EnvironmentError("Supabase credentials are not provided.")

    client = await acreate_client(url, key)
    storage = Storage(client=client, table=table)
    try:
        yield storage
    except StorageException as e:
        print(e)


@app.get(path="/api/user_id/", response_model=Response, status_code=status.HTTP_200_OK)
async def get_user_id():
    return Response(
        message="UserID generated successfully",
        data=UserID(user_id=uuid.uuid4())
    )


@app.get(path="/api/history/{user_id}/", response_model=Response, status_code=status.HTTP_200_OK)
async def get_user_chat_history(storage: Annotated[Storage, Depends(get_storage)], user_id: uuid.UUID):
    messages: list = await storage.get_messages(user_id)
    response = []

    for message in messages:
        _user: dict[str, str] = message["message"]["user"]
        _ai: dict[str, str] = message["message"]["ai"]

        response.append(MessageHistory(
            user=UserMessage(
                message=_user["message"],
                timestamp=_user["timestamp"]
            ),
            ai=AIMessage(
                message=_ai["message"],
                timestamp=_ai["timestamp"],
                mood=_ai["mood"]
            )
        ))

    return Response(message="Message History", data=response)


@app.websocket(path="/chat/{user_id}/")
async def chat(websocket: WebSocket, user_id: uuid.UUID, storage: Annotated[Storage, Depends(get_storage)]):
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

            history: list = await storage.get_messages(user_id, limit=25)

            ai_message: dict[str, Any] = await get_llm_response(history,
                                                                user_message["message"])

            ai_message.update({
                "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
            })

            message = {
                "user": user_message,
                "ai": ai_message
            }

            await storage.add_message(user_id, message)

            await websocket.send_json(data=ai_message)
    except WebSocketDisconnect:
        await websocket.close()
