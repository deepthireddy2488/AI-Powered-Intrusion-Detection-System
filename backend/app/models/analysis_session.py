from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.database.database import Base


class AnalysisSession(Base):
    """One persisted CSV analysis run or live monitoring run."""

    __tablename__ = "analysis_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    source_type = Column(String(30), nullable=False)  # CSV or LIVE
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    completed_at = Column(DateTime, nullable=True)