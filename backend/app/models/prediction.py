from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True, index=True)
    session_id = Column(String(100), nullable=True, index=True)
    row_number = Column(Integer, nullable=True)

    attack_type = Column(String)
    severity = Column(String)
    confidence = Column(Float)
    recommendation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)