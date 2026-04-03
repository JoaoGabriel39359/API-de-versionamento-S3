from fastapi import APIRouter, UploadFile, HTTPException
from services import s3_service, audit
from services.s3_service import S3Service
from services.audit import S3Auditor

router = APIRouter()
s3_service = S3Service() # Uma única instância para o router todo usar
auditor = S3Auditor(s3_service.client, s3_service.bucket_name) 
s3_manager = s3_service


@router.post("/upload/")
async def upload(file: UploadFile):
    content = await file.read()
    response = s3_service.upload(file.filename, content)
    return {"version_id": response.get("VersionId")}

@router.get("/versions/{filename}")
def versions(filename: str):
    res = s3_service.list_versions(filename)
    return res.get('Versions', [])

@router.post("/restore/{filename}/{version_id}")
def restore(filename: str, version_id: str):
    s3_service.restore_version(filename, version_id)
    return {"message": f"Arquivo {filename} restaurado para a versão {version_id}"}

@router.get("/download/{filename}")
def download_file(filename: str, version_id: str = None):
    conteudo = s3_manager.buscar_arquivo(filename, version_id)
    if conteudo is None:
        return {"error": "Arquivo ou versão não encontrada"}
    
    return {"filename": filename, "content": conteudo}

@router.delete("/delete/{filename}")
def delete_file(filename: str):
    try:
        s3_manager.client.delete_object(Bucket=s3_manager.bucket_name, Key=filename)
        return {"message": f"Arquivo {filename} deletado com sucesso (Delete Marker criado)"}
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/audit/{filename}")
def audit_file(filename: str):
    return auditor.gerar_auditoria(filename)