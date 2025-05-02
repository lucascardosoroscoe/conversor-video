from app.services.converter import video_to_audio_ogg
from app.services.storage import upload_to_minio
from app import config
from app.celery_worker import celery
from app.database import SessionLocal
from app.models import Upload
import os

@celery.task(bind=True)
def process_video(self, video_path: str):
    db = SessionLocal()
    upload = db.query(Upload).filter(Upload.task_id == self.request.id).first()
    try:
        upload.status = "STARTED"
        db.merge(upload)
        db.commit()

        video_name = os.path.basename(video_path)
        audio_path = video_path + ".ogg"
        audio_name = video_name + ".ogg"

        upload_to_minio(video_path, config.MINIO_BUCKET_NAME, f"originals/{video_name}")
        upload.original_path = f"originals/{video_name}"

        video_to_audio_ogg(video_path, audio_path)

        upload_to_minio(audio_path, config.MINIO_BUCKET_NAME, f"converted/{audio_name}")
        upload.converted_path = f"converted/{audio_name}"

        upload.status = "SUCCESS"
        db.merge(upload)
        db.commit()
    except Exception as e:
        upload.status = "FAILURE"
        db.merge(upload)
        db.commit()
        raise e
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)
        db.close()