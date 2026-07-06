from fastapi import APIRouter, Depends
from app.dependencies.auth import (
    get_current_user
)
from app.schemas.corte_uni_schema import CorteUniRequest
from app.algorithm.corte_uni import corte_uni, gerar_padroes_guloso

router = APIRouter(
    prefix="/otimizar",
    tags=["Corte Unidimensional"]
)

@router.post(
    "/otimizar",
    summary="Otimizar corte",
    description="Recebe os itens e o comprimento padrão da barra e retorna um plano de corte otimizado com quantidade de barras e desperdício.",
    tags=["Corte Unidimensional"]
)
async def otimizar_corte(
    data: CorteUniRequest, 
    current_user=Depends(get_current_user)):
    
    resultado = corte_uni(
        data.comprimento_padrao,
        data.itens)
    
    return {
        "status_solver": resultado["status_solver"],
        "tempo_execucao_segundos": resultado["tempo_execucao_segundos"],
        "barras_utilizadas": resultado["barras_utilizadas"],
        "desperdicio_total_mm": resultado["desperdicio_total_mm"],
        "plano_de_corte": resultado["plano_de_corte"]
    }
    
    
    
    
    