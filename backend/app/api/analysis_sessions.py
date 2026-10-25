from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import case, func, or_
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.dependencies import get_db
from app.models.attack_log import AttackLog
from app.models.prediction import Prediction
from app.repositories.analysis_session_repository import (
    get_session_by_id,
    get_sessions_by_user,
)
from app.repositories.attack_log_repository import get_attack_logs_by_user
from app.repositories.prediction_repository import get_predictions_by_session

router = APIRouter(prefix="/analysis-sessions", tags=["Analysis Sessions"])


def _is_threat(attack_type: str | None) -> bool:
    return bool(attack_type) and str(attack_type).strip().upper() != "BENIGN"


def _event_title(attack_type: str | None) -> str:
    if _is_threat(attack_type):
        return f"Attack detected: {attack_type}"
    return "Benign traffic classified"


def _query_summary(db: Session, query, attack_column, severity_column) -> dict:
    """Summarize all rows matching the query, not only the current timeline page."""
    filtered_rows = query.with_entities(
        attack_column.label("attack_type"),
        severity_column.label("severity"),
    ).subquery()

    row = (
        db.query(
            func.count().label("total"),
            func.coalesce(
                func.sum(
                    case(
                        (func.upper(filtered_rows.c.attack_type) != "BENIGN", 1),
                        else_=0,
                    )
                ),
                0,
            ).label("threats"),
            func.coalesce(
                func.sum(
                    case(
                        (func.upper(filtered_rows.c.attack_type) == "BENIGN", 1),
                        else_=0,
                    )
                ),
                0,
            ).label("benign"),
            func.coalesce(
                func.sum(
                    case(
                        (func.upper(filtered_rows.c.severity) == "CRITICAL", 1),
                        else_=0,
                    )
                ),
                0,
            ).label("critical"),
        )
        .select_from(filtered_rows)
        .one()
    )

    return {
        "total": int(row.total or 0),
        "threats": int(row.threats or 0),
        "benign": int(row.benign or 0),
        "critical": int(row.critical or 0),
    }


@router.get("/")
def get_analysis_sessions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """List only analysis sessions owned by the signed-in user."""
    return get_sessions_by_user(db=db, user_id=current_user.id)


@router.get("/{session_id}/timeline")
def get_analysis_session_timeline(
    session_id: str,
    severity: str | None = Query(default=None, max_length=30),
    attack_type: str | None = Query(default=None, max_length=100),
    ip_address: str | None = Query(default=None, max_length=100),
    threats_only: bool = Query(default=False),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Return paginated, filtered events for a session owned by the current user."""
    session = get_session_by_id(
        db=db,
        user_id=current_user.id,
        session_id=session_id,
    )
    if not session:
        raise HTTPException(status_code=404, detail="Analysis session not found.")

    if session.source_type.upper() == "CSV":
        query = db.query(Prediction).filter(
            Prediction.user_id == current_user.id,
            Prediction.session_id == session_id,
        )
        if severity:
            query = query.filter(Prediction.severity.ilike(severity))
        if attack_type:
            query = query.filter(Prediction.attack_type.ilike(f"%{attack_type}%"))
        if ip_address:
            # CSV prediction rows do not persist IP addresses, so we cannot
            # truthfully filter them by an IP field.
            raise HTTPException(
                status_code=400,
                detail="IP address filtering is available for live monitoring sessions only.",
            )
        if threats_only:
            query = query.filter(func.upper(Prediction.attack_type) != "BENIGN")

        summary = _query_summary(
            db, query, Prediction.attack_type, Prediction.severity
        )
        rows = (
            query.order_by(Prediction.created_at.desc(), Prediction.id.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        events = []
        for row in rows:
            is_threat = _is_threat(row.attack_type)
            events.append({
                "event_id": f"csv-{row.id}",
                "record_id": row.id,
                "row_number": row.row_number,
                "source_type": "CSV",
                "event_type": "threat" if is_threat else "benign",
                "title": _event_title(row.attack_type),
                "is_threat": is_threat,
                "timestamp": row.created_at,
                "attack_type": row.attack_type,
                "severity": row.severity,
                "confidence": row.confidence,
                "source_ip": None,
                "source_port": None,
                "destination_ip": None,
                "destination_port": None,
                "protocol": None,
                "packet_count": None,
                "status": "Detected" if is_threat else "Normal",
                "recommendation": row.recommendation,
            })

    elif session.source_type.upper() == "LIVE":
        query = db.query(AttackLog).filter(
            AttackLog.user_id == current_user.id,
            AttackLog.session_id == session_id,
        )
        if severity:
            query = query.filter(AttackLog.severity.ilike(severity))
        if attack_type:
            query = query.filter(AttackLog.attack_type.ilike(f"%{attack_type}%"))
        if ip_address:
            ip_pattern = f"%{ip_address.strip()}%"
            query = query.filter(
                or_(
                    AttackLog.source_ip.ilike(ip_pattern),
                    AttackLog.destination_ip.ilike(ip_pattern),
                )
            )
        if threats_only:
            query = query.filter(func.upper(AttackLog.attack_type) != "BENIGN")

        summary = _query_summary(
            db, query, AttackLog.attack_type, AttackLog.severity
        )
        rows = (
            query.order_by(AttackLog.created_at.desc(), AttackLog.id.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        events = []
        for row in rows:
            is_threat = _is_threat(row.attack_type)
            events.append({
                "event_id": f"live-{row.id}",
                "record_id": row.id,
                "row_number": None,
                "source_type": "LIVE",
                "event_type": "threat" if is_threat else "benign",
                "title": _event_title(row.attack_type),
                "is_threat": is_threat,
                "timestamp": row.created_at,
                "attack_type": row.attack_type,
                "severity": row.severity,
                "confidence": row.confidence,
                "source_ip": row.source_ip,
                "source_port": row.source_port,
                "destination_ip": row.destination_ip,
                "destination_port": row.destination_port,
                "protocol": row.protocol,
                "packet_count": row.packet_count,
                "status": row.status,
                "recommendation": row.recommendation,
            })
    else:
        raise HTTPException(status_code=400, detail="Unknown analysis session type.")

    return {
        "session_id": session_id,
        "source_type": session.source_type,
        "session_name": session.name,
        "created_at": session.created_at,
        "completed_at": session.completed_at,
        "total": summary["total"],
        "summary": summary,
        "limit": limit,
        "offset": offset,
        "events": events,
    }


@router.get("/{session_id}")
def get_analysis_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Return aggregate counts and records for one of the user's sessions."""
    session = get_session_by_id(
        db=db,
        user_id=current_user.id,
        session_id=session_id,
    )
    if not session:
        raise HTTPException(status_code=404, detail="Analysis session not found.")

    if session.source_type.upper() == "CSV":
        predictions = get_predictions_by_session(
            db=db,
            user_id=current_user.id,
            session_id=session_id,
        )
        results = [{
            "id": item.id,
            "row": item.row_number,
            "attack": item.attack_type,
            "severity": item.severity,
            "confidence": item.confidence,
            "recommendation": item.recommendation,
            "created_at": item.created_at,
        } for item in predictions]
    elif session.source_type.upper() == "LIVE":
        logs = get_attack_logs_by_user(
            db=db,
            user_id=current_user.id,
            session_id=session_id,
        )
        results = [{
            "id": item.id,
            "attack": item.attack_type,
            "severity": item.severity,
            "confidence": item.confidence,
            "recommendation": item.recommendation,
            "source_ip": item.source_ip,
            "source_port": item.source_port,
            "destination_ip": item.destination_ip,
            "destination_port": item.destination_port,
            "protocol": item.protocol,
            "packet_count": item.packet_count,
            "status": item.status,
            "created_at": item.created_at,
        } for item in logs]
    else:
        raise HTTPException(status_code=400, detail="Unknown analysis session type.")

    total_records = len(results)
    safe_traffic = sum(1 for item in results if str(item["attack"]).upper() == "BENIGN")
    attacks_detected = total_records - safe_traffic

    attack_distribution = {}
    severity_distribution = {}
    for item in results:
        attack = item.get("attack") or "Unknown"
        if str(attack).upper() != "BENIGN":
            attack_distribution[attack] = attack_distribution.get(attack, 0) + 1
        severity = item.get("severity") or "Unknown"
        severity_distribution[severity] = severity_distribution.get(severity, 0) + 1

    return {
        "session": session,
        "total_records": total_records,
        "safe_traffic": safe_traffic,
        "attacks_detected": attacks_detected,
        "attack_distribution": attack_distribution,
        "severity_distribution": severity_distribution,
        "results": results,
    }
