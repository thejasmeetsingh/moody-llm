import uuid
import datetime
from typing import Annotated, Any

from dotenv import dotenv_values
from supabase import acreate_client
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, status
from fastapi.middleware.cors import CORSMiddleware

from llm import get_llm_response
from utils import markdown_to_html
from storage import Storage, StorageException
from schemas import UserID, Response, UserMessage, AIMessage, MessageHistory

app = FastAPI()
app.title = "Moody LLM"
app.description = "A LLM whose mood keeps changing."
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


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

        user_message = MessageHistory(
            message=UserMessage(
                content=_user["content"],
                timestamp=_user["timestamp"]
            ),
            is_user=True
        )

        ai_message = MessageHistory(
            message=AIMessage(
                content=markdown_to_html(_ai["content"]),
                mood=_ai["mood"],
                timestamp=_ai["timestamp"]
            ),
            is_user=False
        )

        response.extend([user_message, ai_message])

    return Response(message="Message History", data=response)


@app.websocket(path="/chat/{user_id}/")
async def chat(websocket: WebSocket, user_id: uuid.UUID, storage: Annotated[Storage, Depends(get_storage)]):
    await websocket.accept()
    try:
        while True:
            user_message: dict[str, Any] = await websocket.receive_json()

            if not user_message.get("content"):
                await websocket.send_denial_response()
                break

            history: list = await storage.get_messages(user_id, limit=25)

            ai_message: dict[str, Any] = await get_llm_response(history,
                                                                user_message["content"])

            ai_message.update({
                "timestamp": round(datetime.datetime.now(datetime.UTC).timestamp())
            })

            message = {
                "user": user_message,
                "ai": ai_message
            }

            await storage.add_message(user_id, message)

            ai_message["content"] = markdown_to_html(ai_message["content"])
            await websocket.send_json(data=ai_message)
    except WebSocketDisconnect:
        await websocket.close()
