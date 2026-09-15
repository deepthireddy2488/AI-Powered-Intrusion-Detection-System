from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.database import Base


class AnalysisSession(Base):

    __tablename__ = "analysis_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # User who owns this session
    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    # Unique session identifier
    session_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    # CSV / LIVE
    source_type = Column(
        String(30),
        nullable=False
    )

    # Display name
    name = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )