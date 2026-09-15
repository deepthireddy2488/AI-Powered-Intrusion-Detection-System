from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4

from app.models.analysis_session import AnalysisSession


def create_analysis_session(
    db: Session,
    user_id: int,
    source_type: str,
    name: str
):
    session_id = str(uuid4())

    session = AnalysisSession(
        user_id=user_id,
        session_id=session_id,
        source_type=source_type,
        name=name
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def complete_analysis_session(
    db: Session,
    session_id: str
):
    session = (
        db.query(AnalysisSession)
        .filter(
            AnalysisSession.session_id == session_id
        )
        .first()
    )

    if session:
        session.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(session)

    return session


def get_sessions_by_user(
    db: Session,
    user_id: int
):
    return (
        db.query(AnalysisSession)
        .filter(
            AnalysisSession.user_id == user_id
        )
        .order_by(
            AnalysisSession.created_at.desc()
        )
        .all()
    )


def get_session_by_id(
    db: Session,
    user_id: int,
    session_id: str
):
    return (
        db.query(AnalysisSession)
        .filter(
            AnalysisSession.user_id == user_id,
            AnalysisSession.session_id == session_id
        )
        .first()
    )