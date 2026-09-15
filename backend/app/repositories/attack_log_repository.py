from sqlalchemy.orm import Session

from app.models.attack_log import AttackLog


def create_attack_log(
    db: Session,
    source_ip: str,
    destination_ip: str,
    attack_type: str,
    severity: str,
    user_id: int,
    session_id: str,
    status: str = "Detected"
):

    attack_log = AttackLog(
        source_ip=source_ip,
        destination_ip=destination_ip,
        attack_type=attack_type,
        severity=severity,
        user_id=user_id,
        session_id=session_id,
        status=status
    )

    db.add(attack_log)
    db.commit()
    db.refresh(attack_log)

    print("===================================")
    print("DATABASE INSERT SUCCESS")
    print("ID:", attack_log.id)
    print("User ID:", attack_log.user_id)
    print("Session ID:", attack_log.session_id)
    print("Attack:", attack_log.attack_type)
    print("Source:", attack_log.source_ip)
    print("===================================")

    return attack_log


def get_attack_logs_by_user(
    db: Session,
    user_id: int,
    session_id: str = None
):

    query = db.query(AttackLog).filter(
        AttackLog.user_id == user_id
    )

    if session_id:
        query = query.filter(
            AttackLog.session_id == session_id
        )

    return (
        query
        .order_by(AttackLog.id.desc())
        .all()
    )