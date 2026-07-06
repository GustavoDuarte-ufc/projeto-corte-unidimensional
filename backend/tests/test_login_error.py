import asyncio

import pytest
from fastapi import HTTPException

from app.api.auth import login
from app.schemas.user_schema import UserLogin


def test_login_error():
    async def _call_login():
        return await login(
            UserLogin(email="naoexiste@email.com", password="senhaerrada")
        )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(_call_login())

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Email ou senha inválidos"
