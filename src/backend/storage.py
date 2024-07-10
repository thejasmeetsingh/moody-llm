import uuid

from supabase import AClient


class Storage:
    """
    Supabase storage module
    """

    def __init__(self, client: AClient, table: str) -> None:
        self.table = table
        self.client = client

    async def get_messages(self, user_id: uuid.UUID, limit: int | None = None):
        """
        Retrieve chat message history from supabase (latest on top)
        """

        query = self.client.table(self.table).select("message").eq(
            "user_id", str(user_id)).order("created_at", desc=True)

        if limit is not None:
            query = query.limit(limit)

        response = await query.execute()
        return response.data

    async def add_message(self, user_id: uuid.UUID, message: dict):
        """
        Create message record in supabase
        """

        await self.client.table(self.table).insert({
            "user_id": str(user_id),
            "message": message
        }).execute()


class StorageException(Exception):
    """
    Custom storage exception
    """
