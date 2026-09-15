from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.attack_log_repository import (
    get_attack_logs_by_user
)
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/attack-logs",
    tags=["Attack Logs"]
)


# ============================================
# CURRENT USER / CURRENT SESSION LOGS
# ============================================

@router.get("/")
def get_attack_logs(
    session_id: str = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    logs = get_attack_logs_by_user(
        db=db,
        user_id=current_user.id,
        session_id=session_id
    )

    return logs


# ============================================
# CURRENT USER - COMPLETE HISTORY
# ============================================

@router.get("/history")
def get_attack_log_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    logs = get_attack_logs_by_user(
        db=db,
        user_id=current_user.id
    )

    return logs