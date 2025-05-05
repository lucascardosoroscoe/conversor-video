from fastapi import APIRouter, File, UploadFile, HTTPException
from tempfile import NamedTemporaryFile
import shutil, os
from app.tasks import process_video
from app.celery_worker import celery
from app.database import SessionLocal
from app.models import Upload
from app import config


base_url = config.MINIO_URL.rstrip("/") + '/' + config.MINIO_BUCKET_NAME + '/'


router = APIRouter()

@router.post("/upload-video")
def upload_video(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="Nenhum arquivo enviado.")
    suffix = os.path.splitext(file.filename)[1]
    try:
        tmp_video = NamedTemporaryFile(delete=False, suffix=suffix)
        shutil.copyfileobj(file.file, tmp_video)
    finally:
        tmp_video_path = tmp_video.name
        tmp_video.close()
        file.file.close()

    task = process_video.delay(tmp_video_path)

    db = SessionLocal()
    upload = Upload(task_id=task.id, filename=file.filename)
    db.add(upload)
    db.commit()
    db.close()

    return {"message": "Vídeo enviado para processamento em background.", "task_id": task.id}

@router.get("/task-status/{task_id}")
def task_status(task_id: str):
    task_result = celery.AsyncResult(task_id)
    db = SessionLocal()
    upload = db.query(Upload).filter(Upload.task_id == task_id).first()
    db.close()
    return {
        "task_id": task_id,
        "status": upload.status if upload else task_result.status,
        "filename": upload.filename if upload else None,
        "original_path": base_url + upload.original_path if upload else None,
        "converted_path": base_url + upload.converted_path if upload else None
    }