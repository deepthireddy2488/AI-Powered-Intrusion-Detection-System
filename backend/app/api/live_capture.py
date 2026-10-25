from threading import RLock, Thread

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.database import SessionLocal
from app.database.dependencies import get_db
from app.repositories.analysis_session_repository import (
    complete_analysis_session,
    create_analysis_session,
)
from app.services.live_capture import start_capture, stop_capture

router = APIRouter(prefix="/live-capture", tags=["Live Capture"])

_capture_lock = RLock()
capture_thread = None
current_session_id = None
current_user_id = None


def _capture_worker(user_id: int, session_id: str):
    """Run capture and mark its session complete even if sniffing errors."""
    try:
        start_capture(
            interface=None,
            timeout=None,
            user_id=user_id,
            session_id=session_id,
        )
    finally:
        db = SessionLocal()
        try:
            complete_analysis_session(
                db=db,
                user_id=user_id,
                session_id=session_id,
            )
        except Exception as error:
            db.rollback()
            print(f"Could not mark live session complete: {error}")
        finally:
            db.close()


@router.post("/start")
def start_live_capture(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    global capture_thread, current_session_id, current_user_id

    with _capture_lock:
        if capture_thread and capture_thread.is_alive():
            if current_user_id != current_user.id:
                raise HTTPException(
                    status_code=409,
                    detail="Live monitoring is already running for another user.",
                )
            return {
                "message": "Live capture is already running",
                "session_id": current_session_id,
            }

        analysis_session = create_analysis_session(
            db=db,
            user_id=current_user.id,
            source_type="LIVE",
            name="Live Monitoring",
        )
        current_session_id = analysis_session.session_id
        current_user_id = current_user.id

        capture_thread = Thread(
            target=_capture_worker,
            args=(current_user.id, current_session_id),
            daemon=True,
            name=f"ids-capture-{current_session_id[:8]}",
        )
        capture_thread.start()

    return {
        "message": "Live capture started successfully",
        "session_id": current_session_id,
    }


@router.post("/stop")
def stop_live_capture(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    with _capture_lock:
        thread = capture_thread
        session_id = current_session_id
        owner_id = current_user_id

    if not thread or owner_id != current_user.id:
        if owner_id is not None and owner_id != current_user.id and thread and thread.is_alive():
            raise HTTPException(
                status_code=403,
                detail="You cannot stop another user's live monitoring session.",
            )
        return {
            "message": "No active monitoring session for this user.",
            "session_id": session_id if owner_id == current_user.id else None,
        }

    if not thread.is_alive():
        complete_analysis_session(
            db=db,
            user_id=current_user.id,
            session_id=session_id,
        )
        return {
            "message": "Live capture is already stopped",
            "session_id": session_id,
        }

    # stop_capture() is synchronous and handles the no-new-packets case too.
    stop_capture()
    thread.join(timeout=10)
    if thread.is_alive():
        raise HTTPException(
            status_code=504,
            detail="Capture stop was requested but the worker has not exited yet. Check backend logs.",
        )

    complete_analysis_session(
        db=db,
        user_id=current_user.id,
        session_id=session_id,
    )
    return {
        "message": "Live capture stopped successfully",
        "session_id": session_id,
    }


@router.get("/status")
def get_live_capture_status(current_user=Depends(get_current_user)):
    with _capture_lock:
        thread = capture_thread
        session_id = current_session_id
        owner_id = current_user_id

    if thread and thread.is_alive():
        if owner_id != current_user.id:
            return {
                "status": "stopped",
                "message": "No active monitoring session for this user.",
                "session_id": None,
            }
        return {
            "status": "running",
            "message": "Live capture is currently running",
            "session_id": session_id,
        }

    if owner_id == current_user.id and session_id:
        return {
            "status": "stopped",
            "message": "Live capture is currently stopped",
            "session_id": session_id,
        }

    return {
        "status": "stopped",
        "message": "No monitoring session available.",
        "session_id": None,
    }