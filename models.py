from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class AudioSample(Base):
    __tablename__ = "audio_samples"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
