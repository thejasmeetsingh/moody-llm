import uuid

from fastapi import FastAPI, status

from schemas import UserID, Response


app = FastAPI()
app.title = "Moody LLM"
app.description = "A LLM whose mood keeps changing."


@app.get(path="/api/user_id", response_model=Response, status_code=status.HTTP_200_OK)
async def get_user_id():
    return Response(
        message="UserID generated successfully",
        data=UserID(user_id=uuid.uuid4())
    )
