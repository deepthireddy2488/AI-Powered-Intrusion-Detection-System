from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.attack_log_repository import get_all_attack_logs


router = APIRouter(
    prefix="/attack-logs",
    tags=["Attack Logs"]
)


@router.get("/")
def get_attack_logs(
    db: Session = Depends(get_db)
):

    logs = get_all_attack_logs(db)

    return logs