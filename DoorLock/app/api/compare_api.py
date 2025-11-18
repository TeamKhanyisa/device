from fastapi import APIRouter, UploadFile, File
from app.services.compare_service import verify_face

router = APIRouter()

@router.post("/api/verify_face")
async def api_verify_face(file: UploadFile = File(...)):
    file_bytes = await file.read()
    result = verify_face(file_bytes)
    return result
