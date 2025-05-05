from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import SessionLocal
from app.models import Upload
from typing import Optional
from datetime import datetime
from fastapi import HTTPException
from app import config

base_url = config.MINIO_URL.rstrip("/") + '/' + config.MINIO_BUCKET_NAME + '/'


router = APIRouter()


@router.get("/uploads")
def list_uploads(
    status: Optional[str] = Query(None),
    filename: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    skip: int = 0,
    limit: int = 100
):
    db: Session = SessionLocal()
    query = db.query(Upload)

    filters = []
    if status:
        filters.append(Upload.status == status)
    if filename:
        filters.append(Upload.filename.ilike(f"%{filename}%"))
    if start_date:
        filters.append(Upload.created_at >= start_date)
    if end_date:
        filters.append(Upload.created_at <= end_date)

    if filters:
        query = query.filter(and_(*filters))

    results = query.order_by(Upload.created_at.desc()).offset(skip).limit(limit).all()
    db.close()
    return [
        {
            "task_id": u.task_id,
            "filename": u.filename,
            "status": u.status,
            "original_path": base_url + u.original_path if u.original_path else None,
            "converted_path": base_url + u.converted_path if u.converted_path else None,
            "created_at": u.created_at
        } for u in results
    ]