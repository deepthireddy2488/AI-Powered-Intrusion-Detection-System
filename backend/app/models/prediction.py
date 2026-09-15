from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database.database import Base


class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # User who owns this prediction
    user_id = Column(
        Integer,
        nullable=True,
        index=True
    )

    # Analysis session this prediction belongs to
    session_id = Column(
        String(100),
        nullable=True,
        index=True
    )

    attack_type = Column(String)

    severity = Column(String)

    confidence = Column(Float)

    recommendation = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )