import asyncio
import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient


def test_mongodb_connection():
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        pytest.skip("MONGO_URI não configurado")

    async def _ping():
        client = AsyncIOMotorClient(mongo_uri)
        try:
            return await client.admin.command("ping")
        finally:
            client.close()

    try:
        result = asyncio.run(_ping())
    except Exception as exc:
        pytest.fail(f"Falha ao conectar ao MongoDB: {exc}")

    assert result.get("ok") == 1
