from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user

from app.services.session_service import (
    get_user_sessions,
    revoke_all_sessions
)

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)

@router.get("/", summary="Listar sessões", description="Retorna todas as sessões ativas vinculadas ao usuário autenticado.", tags=["Sessions"])
async def list_sessions(
        current_user=Depends(
            get_current_user
        )):

    sessions = await get_user_sessions(
        str(current_user["_id"])
    )

    return sessions

@router.delete("/all", summary="Revogar todas as sessões", description="Encerra todas as sessões ativas do usuário autenticado de uma vez.", tags=["Sessions"])
async def logout_all(
        current_user=Depends(
            get_current_user
        )):

    await revoke_all_sessions(
        str(current_user["_id"])
    )

    return {
        "message":
            "Todas as sessões foram encerradas"
    }
    