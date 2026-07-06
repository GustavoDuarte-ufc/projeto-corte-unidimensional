import asyncio
from unittest.mock import AsyncMock, patch

from app.schemas.user_schema import UserLogin


def test_login_success():
    async def _run():
        fake_db_user = {
            "_id": "user-123",
            "email": "teste@gmail.com",
            "password": "hashed-password",
            "role": "user",
        }

        with patch("app.services.auth_service.users_collection.find_one", new=AsyncMock(return_value=fake_db_user)), \
             patch("app.services.auth_service.verify_password", return_value=True), \
             patch("app.services.auth_service.create_access_token", return_value="access-token"), \
             patch("app.services.auth_service.create_refresh_token", return_value="refresh-token"), \
             patch("app.services.auth_service.create_session", new=AsyncMock(return_value=None)):
            from app.services.auth_service import login_user

            tokens = await login_user(UserLogin(email="teste@gmail.com", password="123456"))

        assert tokens is not None
        assert tokens["access_token"] == "access-token"
        assert tokens["refresh_token"] == "refresh-token"

    asyncio.run(_run())

