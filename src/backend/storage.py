import uuid

from supabase import AClient


class Storage:
    def __init__(self, client: AClient, table: str) -> None:
        self.table = table
        self.client = client

    async def get_messages(self, user_id: uuid.UUID, limit: int | None = None):
        query = self.client.table(self.table).\
            select("message").\
            eq("user_id", str(user_id))

        if limit is not None:
            query = query.limit(limit)

        response = await query.order("created_at").execute()
        return response.data

    async def add_message(self, user_id: uuid.UUID, message: dict):
        await self.client.table(self.table).insert({
            "user_id": str(user_id),
            "message": message
        }).execute()


class StorageException(Exception):
    pass
