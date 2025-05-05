from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Upload(Base):
    __tablename__ = "uploads"
    task_id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    original_path = Column(String, nullable=True)
    converted_path = Column(String, nullable=True)
    transcription = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="PENDING")