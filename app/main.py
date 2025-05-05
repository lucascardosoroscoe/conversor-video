from fastapi import FastAPI
from app.api import video, uploads
app = FastAPI()
app.include_router(video.router)
app.include_router(uploads.router)