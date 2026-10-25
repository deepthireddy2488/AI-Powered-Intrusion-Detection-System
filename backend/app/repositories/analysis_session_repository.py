from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.analysis_session import AnalysisSession


def create_analysis_session(db: Session, user_id: int, source_type: str, name: str):
    session = AnalysisSession(
        user_id=user_id,
        session_id=str(uuid4()),
        source_type=source_type.upper(),
        name=name,
    )
    try:
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    except Exception:
        db.rollback()
        raise


def complete_analysis_session(db: Session, session_id: str, user_id: int | None = None):
    query = db.query(AnalysisSession).filter(AnalysisSession.session_id == session_id)
    if user_id is not None:
        query = query.filter(AnalysisSession.user_id == user_id)
    session = query.first()
    if session is not None and session.completed_at is None:
        session.completed_at = datetime.utcnow()
        try:
            db.commit()
            db.refresh(session)
        except Exception:
            db.rollback()
            raise
    return session


def get_sessions_by_user(db: Session, user_id: int):
    return (
        db.query(AnalysisSession)
        .filter(AnalysisSession.user_id == user_id)
        .order_by(AnalysisSession.created_at.desc(), AnalysisSession.id.desc())
        .all()
    )


def get_session_by_id(db: Session, user_id: int, session_id: str):
    return (
        db.query(AnalysisSession)
        .filter(
            AnalysisSession.user_id == user_id,
            AnalysisSession.session_id == session_id,
        )
        .first()
    )
