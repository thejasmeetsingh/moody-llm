import os
import uuid

from supabase import AClient, acreate_client


table = os.getenv("SUPABASE_TABLE_NAME")
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not table or not url or not key:
    raise EnvironmentError("Supabase credentials are not provided.")


async def get_client():
    client = await acreate_client(url, key)
    try:
        yield client
    except Exception as _:
        pass


async def get_messages(client: AClient, user_id: uuid.UUID, limit: int | None = None) -> dict[str, list]:
    query = client.table(table).select("message").eq("user_id", user_id)
    if limit is not None:
        query = query.limit(limit)

    return await query.order("created_at", desc=True).execute()


async def add_message(client: AClient, user_id: uuid.UUID, message: dict) -> None:
    await client.table(table).insert({
        "user_id": user_id,
        "message": message
    }).execute()
