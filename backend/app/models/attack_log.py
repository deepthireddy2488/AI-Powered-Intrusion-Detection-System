from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.database import Base


class AttackLog(Base):

    __tablename__ = "attack_logs"

    id = Column(Integer, primary_key=True, index=True)

    # User who owns this record
    user_id = Column(Integer, nullable=True, index=True)

    # Unique ID for each live monitoring session
    session_id = Column(String(100), nullable=True, index=True)

    source_ip = Column(String(50), nullable=False)

    destination_ip = Column(String(50), nullable=False)

    attack_type = Column(String(100), nullable=False)

    severity = Column(String(20), nullable=False)

    status = Column(String(20), default="Detected")

    created_at = Column(DateTime, default=datetime.utcnow)