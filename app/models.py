# backend/app/models.py

from sqlalchemy import Column, Integer, Text, DateTime, func
from .database import Base

class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, index=True)
    symptoms = Column(Text, nullable=False)
    diagnosis_response = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())