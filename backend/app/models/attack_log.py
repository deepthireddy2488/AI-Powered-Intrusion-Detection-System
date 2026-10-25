from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from app.database.database import Base


class AttackLog(Base):
    __tablename__ = "attack_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True, index=True)
    session_id = Column(String(100), nullable=True, index=True)

    source_ip = Column(String(50), nullable=False)
    destination_ip = Column(String(50), nullable=False)
    source_port = Column(Integer, nullable=True)
    destination_port = Column(Integer, nullable=True)
    protocol = Column(String(10), nullable=True)

    attack_type = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False)
    status = Column(String(20), default="Detected")

    # Confidence is stored as a percentage from 0 to 100.
    confidence = Column(Float, nullable=True)
    packet_count = Column(Integer, nullable=True)
    recommendation = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
