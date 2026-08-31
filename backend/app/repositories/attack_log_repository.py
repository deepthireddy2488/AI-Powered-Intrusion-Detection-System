from sqlalchemy.orm import Session

from app.models.attack_log import AttackLog


def create_attack_log(
    db: Session,
    source_ip: str,
    destination_ip: str,
    attack_type: str,
    severity: str,
    status: str = "Detected"
):

    attack_log = AttackLog(
        source_ip=source_ip,
        destination_ip=destination_ip,
        attack_type=attack_type,
        severity=severity,
        status=status
    )

    db.add(attack_log)
    db.commit()
    db.refresh(attack_log)

    print("===================================")
    print("DATABASE INSERT SUCCESS")
    print("ID:", attack_log.id)
    print("Attack:", attack_log.attack_type)
    print("Source:", attack_log.source_ip)
    print("===================================")

    return attack_log


def get_all_attack_logs(db: Session):

    return (
        db.query(AttackLog)
        .order_by(AttackLog.id.desc())
        .all()
    )