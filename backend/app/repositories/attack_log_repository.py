from sqlalchemy.orm import Session

from app.models.attack_log import AttackLog


def create_attack_log(
    db: Session,
    source_ip: str,
    destination_ip: str,
    attack_type: str,
    severity: str,
    user_id: int | None = None,
    session_id: str | None = None,
    status: str = "Detected",
    source_port: int | None = None,
    destination_port: int | None = None,
    protocol: str | None = None,
    packet_count: int | None = None,
    confidence: float | None = None,
    recommendation: str | None = None,
):
    """Persist one flow classification with enough context for investigation."""
    log = AttackLog(
        source_ip=source_ip,
        destination_ip=destination_ip,
        source_port=source_port,
        destination_port=destination_port,
        protocol=protocol,
        attack_type=attack_type,
        severity=severity,
        status=status,
        user_id=user_id,
        session_id=session_id,
        packet_count=packet_count,
        confidence=confidence,
        recommendation=recommendation,
    )
    try:
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    except Exception:
        db.rollback()
        raise


def get_attack_logs_by_user(db: Session, user_id: int, session_id: str | None = None):
    query = db.query(AttackLog).filter(AttackLog.user_id == user_id)
    if session_id:
        query = query.filter(AttackLog.session_id == session_id)
    return query.order_by(AttackLog.created_at.desc(), AttackLog.id.desc()).all()
