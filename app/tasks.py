from app.services.converter import video_to_audio_ogg
from app.services.storage import upload_to_minio, download_from_minio
from app import config
from app.celery_worker import celery
from app.database import SessionLocal
from app.models import Upload
import os
import hashlib
import whisper

@celery.task(bind=True)
def process_video(self, video_path: str):
    print("🚀 Tarefa process_video iniciada")
    print(f"📁 Caminho recebido: {video_path}")
    db = SessionLocal()
    upload = db.query(Upload).filter(Upload.task_id == self.request.id).first()
    
    if not upload:
        print("❌ Tarefa não registrada no banco. Cancelando.")
        db.close()
        return

    audio_path = None

    try:
        upload.status = "STARTED"
        db.merge(upload)
        db.commit()

        # Hash baseado no nome do arquivo + task_id
        video_name = os.path.basename(video_path)
        simple_hash = hashlib.sha256(f"{video_name}-{self.request.id}".encode()).hexdigest()

        video_ext = os.path.splitext(video_name)[1]
        original_object_name = f"originals/{simple_hash}{video_ext}"
        converted_object_name = f"converted/{simple_hash}.ogg"
        audio_path = f"/tmp/{simple_hash}.ogg"

        print("📤 Enviando vídeo original para o MinIO...")
        upload_to_minio(video_path, config.MINIO_BUCKET_NAME, original_object_name)
        upload.original_path = original_object_name

        print("🎧 Convertendo com FFmpeg...")
        video_to_audio_ogg(video_path, audio_path)

        print("📤 Enviando áudio convertido para o MinIO...")
        upload_to_minio(audio_path, config.MINIO_BUCKET_NAME, converted_object_name)
        upload.converted_path = converted_object_name

        upload.status = "SUCCESS"
        db.merge(upload)
        db.commit()

        print("✅ Finalizando tarefa de conversão com sucesso")

        # Chama transcrição como task encadeada
        print("🤖 Rodando Whisper para transcrever...")
        model = whisper.load_model("base")

        local_audio = f"/tmp/transcribe_{upload.task_id}.ogg"

        print("📥 Baixando áudio para transcrição...")
        download_from_minio(config.MINIO_BUCKET_NAME, upload.converted_path, local_audio)

        print("🤖 Rodando Whisper para transcrever...")
        model = whisper.load_model("base")
        result = model.transcribe(local_audio)
        transcription = result["text"]
        upload.transcription = transcription
        print("📝 Resultado completo:", transcription)
        upload.status = "TRANSCRIBED"
        db.merge(upload)
        db.commit()

        print("✅ Transcrição concluída com sucesso")

    except Exception as e:
        upload.status = "FAILURE"
        db.merge(upload)
        db.commit()
        print(f"❌ Erro na task process_video: {e}")
        raise e
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(local_audio):
            os.remove(local_audio)
        db.close()

