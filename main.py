from fastapi import FastAPI
from routes.routes import router as s3_router
from routes.routes import s3_service  

app = FastAPI(
    title="API de versão S3 com FastAPI", 
    description="Exemplo de API para gerenciar versões de arquivos S3."
)

app.include_router(s3_router, prefix="/v1", tags=["S3 Operations"])

@app.on_event("startup")
def startup():
    s3_service.setup_bucket()

@app.get("/")
def read_root():
    return {"message": "API Rodando com Sucesso!"}