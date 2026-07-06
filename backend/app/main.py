from fastapi import FastAPI

from app.database.mongodb import database
from app.api.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.corte_uni import router as corte_uni_router

from app.api.sessions import (
    router as sessions_router
)

app = FastAPI(
    title="Corte Unidimensional API",
    description="API para autenticação e otimização de corte unidimensional com suporte a sessões JWT e solver de otimização.",
    version="1.0.0",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Cadastro, login, refresh e logout de usuários."
        },
        {
            "name": "Sessions",
            "description": "Consulta e revogação de sessões ativas do usuário."
        },
        {
            "name": "Corte Unidimensional",
            "description": "Geração de padrões e otimização de corte para barras unidimensionais."
        }
    ]
)

app.include_router(auth_router)
app.include_router(sessions_router)
app.include_router(corte_uni_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", summary="Status da API", description="Retorna uma confirmação de funcionamento da API.", tags=["Health"])
async def home():
    return {
        "message": "API funcionando"
    }


@app.get("/test-db", summary="Conexão com o banco", description="Verifica a conexão com o banco de dados MongoDB e lista as coleções disponíveis.", tags=["Health"])
async def test_db():

    collections = await database.list_collection_names()

    return {
        "database": "conectado",
        "collections": collections
    }