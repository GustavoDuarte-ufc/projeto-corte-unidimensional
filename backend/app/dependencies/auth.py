from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import verify_token
from app.database.mongodb import users_collection

security = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    user = await users_collection.find_one(
        {"email": payload["email"]}
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    return user