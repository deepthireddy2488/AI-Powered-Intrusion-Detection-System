from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.dependencies import get_current_user

from app.repositories.analysis_session_repository import (
    get_sessions_by_user,
    get_session_by_id
)

from app.repositories.prediction_repository import (
    get_predictions_by_session
)

from app.repositories.attack_log_repository import (
    get_attack_logs_by_user
)


router = APIRouter(
    prefix="/analysis-sessions",
    tags=["Analysis Sessions"]
)


# ==========================================
# GET ALL SESSIONS FOR CURRENT USER
# ==========================================

@router.get("/")
def get_analysis_sessions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    sessions = get_sessions_by_user(
        db=db,
        user_id=current_user.id
    )

    return sessions


# ==========================================
# GET ONE SESSION DETAILS
# ==========================================

@router.get("/{session_id}")
def get_analysis_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    session = get_session_by_id(
        db=db,
        user_id=current_user.id,
        session_id=session_id
    )

    if not session:

        raise HTTPException(
            status_code=404,
            detail="Analysis session not found."
        )


    # ==========================================
    # CSV SESSION
    # ==========================================

    if session.source_type == "CSV":

        predictions = get_predictions_by_session(
            db=db,
            user_id=current_user.id,
            session_id=session_id
        )

        results = []

        for prediction in predictions:

            results.append({
                "id": prediction.id,
                "attack": prediction.attack_type,
                "severity": prediction.severity,
                "confidence": prediction.confidence,
                "recommendation": prediction.recommendation,
                "created_at": prediction.created_at
            })


        total_records = len(results)

        safe_traffic = sum(
            1
            for item in results
            if item["attack"] == "BENIGN"
        )

        attacks_detected = sum(
            1
            for item in results
            if item["attack"] != "BENIGN"
        )


        attack_counts = {}

        for item in results:

            attack = item["attack"]

            if attack != "BENIGN":

                attack_counts[attack] = (
                    attack_counts.get(attack, 0) + 1
                )


        severity_counts = {}

        for item in results:

            severity = item["severity"]

            severity_counts[severity] = (
                severity_counts.get(severity, 0) + 1
            )


        return {
            "session": session,
            "total_records": total_records,
            "safe_traffic": safe_traffic,
            "attacks_detected": attacks_detected,
            "attack_distribution": attack_counts,
            "severity_distribution": severity_counts,
            "results": results
        }


    # ==========================================
    # LIVE SESSION
    # ==========================================

    elif session.source_type == "LIVE":

        logs = get_attack_logs_by_user(
            db=db,
            user_id=current_user.id,
            session_id=session_id
        )

        total_records = len(logs)

        safe_traffic = sum(
            1
            for log in logs
            if log.attack_type == "BENIGN"
        )

        attacks_detected = sum(
            1
            for log in logs
            if log.attack_type != "BENIGN"
        )


        attack_counts = {}

        for log in logs:

            attack = log.attack_type

            if attack != "BENIGN":

                attack_counts[attack] = (
                    attack_counts.get(attack, 0) + 1
                )


        severity_counts = {}

        for log in logs:

            severity = log.severity

            severity_counts[severity] = (
                severity_counts.get(severity, 0) + 1
            )


        results = []

        for log in logs:

            results.append({
                "id": log.id,
                "attack": log.attack_type,
                "severity": log.severity,
                "source_ip": log.source_ip,
                "destination_ip": log.destination_ip,
                "status": log.status,
                "created_at": log.created_at
            })


        return {
            "session": session,
            "total_records": total_records,
            "safe_traffic": safe_traffic,
            "attacks_detected": attacks_detected,
            "attack_distribution": attack_counts,
            "severity_distribution": severity_counts,
            "results": results
        }


    raise HTTPException(
        status_code=400,
        detail="Unknown session type."
    )