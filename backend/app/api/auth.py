from fastapi import APIRouter, HTTPException

from app.schemas.user_schema import UserRegister
from app.services.auth_service import create_user

from fastapi import Depends
from app.dependencies.auth import get_current_user

from app.database.mongodb import sessions_collection

from app.core.security import (
    verify_token,
    create_access_token,
    hash_refresh_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    summary="Registrar usuário",
    description="Cria uma nova conta no sistema com nome, e-mail e senha.",
    tags=["Authentication"]
)
async def register(user: UserRegister):

    created = await create_user(user)

    if not created:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )

    return {
        "message": "Usuário criado com sucesso",
        "user_id": created
    }
    

from app.schemas.user_schema import (
    UserRegister,
    UserLogin
)

from app.services.auth_service import (
    create_user,
    login_user
)

@router.post(
    "/login",
    summary="Autenticar usuário",
    description="Valida as credenciais do usuário e retorna tokens de acesso e refresh.",
    tags=["Authentication"]
)
async def login(user: UserLogin):

    tokens = await login_user(user)

    if not tokens:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        )

    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer"
    }
    
@router.get(
    "/me",
    summary="Dados do usuário autenticado",
    description="Retorna as informações do usuário autenticado baseado no token de acesso.",
    tags=["Authentication"]
)
async def me(current_user=Depends(get_current_user)):

    return {
        "id": str(current_user["_id"]),
        "name": current_user["name"],
        "email": current_user["email"],
        "role": current_user["role"]
    }

@router.post(
    "/refresh",
    summary="Renovar token",
    description="Gera um novo access token a partir de um refresh token válido.",
    tags=["Authentication"]
)
async def refresh_token(data: dict):

    refresh = data["refresh_token"]

    # 1. Validar o JWT
    payload = verify_token(refresh)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Refresh token inválido"
        )

    # 2. Garantir que é um refresh token
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Token incorreto"
        )

    # 3. Procurar a sessão no MongoDB
    session = await sessions_collection.find_one(
        {
            "refresh_token_hash":
                hash_refresh_token(refresh),
            "revoked": False
        }
    )

    # 4. Verificar se a sessão existe
    if not session:
        raise HTTPException(
            status_code=401,
            detail="Sessão inválida"
        )

    # 5. Gerar novo access token
    new_access = create_access_token({
        "sub": payload["sub"],
        "email": payload["email"],
        "role": payload["role"]
    })

    return {
        "access_token": new_access,
        "token_type": "bearer"
    }

@router.post(
    "/logout",
    summary="Encerrar sessão",
    description="Revoga a sessão associada ao refresh token informado.",
    tags=["Authentication"]
)
async def logout(data: dict):

    await sessions_collection.update_one(
        {
            "refresh_token_hash":
                hash_refresh_token(
                    data["refresh_token"]
                )
        },
        {
            "$set": {
                "revoked": True
            }
        }
    )

    return {
        "message":
            "Logout realizado"
    }