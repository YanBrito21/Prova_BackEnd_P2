from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routers import router

app = FastAPI(
    title="API de Gerenciamento de Produtos",
    description="Desafio de FastAPI com PostgreSQL via Docker",
    version="1.0.0"
)

# 🔥 A MELHORIA: Intercepta erros de validação do Pydantic (422) e limpa a resposta
@app.exception_handler(RequestValidationError)
def validacao_exception_handler(request: Request, exc: RequestValidationError):
    # Captura apenas a primeira mensagem de erro amigável gerada
    erros_formatados = []
    for error in exc.errors():
        campo = " -> ".join([str(loc) for loc in error["loc"] if loc != "body"])
        mensagem = error["msg"]
        erros_formatados.append(f"Erro no campo [{campo}]: {mensagem}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "erro",
            "mensagem": "Dados de entrada inválidos.",
            "detalhes": erros_formatados
        }
    )

# Inclui as rotas
app.include_router(router)