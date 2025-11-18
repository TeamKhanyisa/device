from fastapi import APIRouter, UploadFile, File, Form
from app.services.register_service import register_face_step

router = APIRouter()

@router.post("/api/register_face_step")
async def register_face_api(step: int = Form(...), file: UploadFile = File(...)):
    file_bytes = await file.read()
    return register_face_step(step=step, file_bytes=file_bytes)
