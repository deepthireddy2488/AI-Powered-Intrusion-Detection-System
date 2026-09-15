from fastapi import APIRouter, Depends, HTTPException
from threading import Thread
from uuid import uuid4
from sqlalchemy.orm import Session

from app.services.live_capture import start_capture, stop_capture
from app.core.dependencies import get_current_user
from app.database.dependencies import get_db

from app.repositories.analysis_session_repository import (
    create_analysis_session,
    complete_analysis_session
)


router = APIRouter(
    prefix="/live-capture",
    tags=["Live Capture"]
)


# ============================================
# GLOBAL CAPTURE THREAD
# ============================================

capture_thread = None


# Currently running/latest session
current_session_id = None
current_user_id = None


# ============================================
# START LIVE CAPTURE
# ============================================

@router.post("/start")
def start_live_capture(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    global capture_thread
    global current_session_id
    global current_user_id

    # --------------------------------------------
    # Check if capture is already running
    # --------------------------------------------

    if capture_thread and capture_thread.is_alive():

        # Prevent another user from taking over
        if current_user_id != current_user.id:

            raise HTTPException(
                status_code=409,
                detail="Live monitoring is already running for another user."
            )

        return {
            "message": "Live capture is already running",
            "session_id": current_session_id
        }

    # --------------------------------------------
    # Create NEW session ID
    # --------------------------------------------

    session_id = str(uuid4())

    # --------------------------------------------
    # Save LIVE session in database
    # --------------------------------------------

    analysis_session = create_analysis_session(
        db=db,
        user_id=current_user.id,
        source_type="LIVE",
        name="Live Monitoring"
    )

    # Use the database-created session ID
    session_id = analysis_session.session_id

    current_session_id = session_id
    current_user_id = current_user.id

    # --------------------------------------------
    # Start background capture
    # --------------------------------------------

    capture_thread = Thread(
        target=start_capture,
        kwargs={
            "interface": None,
            "timeout": None,
            "user_id": current_user.id,
            "session_id": session_id
        },
        daemon=True
    )

    capture_thread.start()

    return {
        "message": "Live capture started successfully",
        "session_id": session_id
    }


# ============================================
# STOP LIVE CAPTURE
# ============================================

@router.post("/stop")
def stop_live_capture(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    global capture_thread
    global current_session_id
    global current_user_id

    # --------------------------------------------
    # Check if running
    # --------------------------------------------

    if not capture_thread or not capture_thread.is_alive():

        return {
            "message": "Live capture is not running",
            "session_id": current_session_id
        }

    # --------------------------------------------
    # Only owner can stop
    # --------------------------------------------

    if current_user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="You cannot stop another user's live monitoring session."
        )

    # --------------------------------------------
    # Remember completed session
    # --------------------------------------------

    stopped_session_id = current_session_id

    # --------------------------------------------
    # Stop packet capture
    # --------------------------------------------

    stop_capture()

    # --------------------------------------------
    # Mark database session as completed
    # --------------------------------------------

    complete_analysis_session(
        db=db,
        session_id=stopped_session_id
    )

    # --------------------------------------------
    # IMPORTANT:
    # Do NOT clear current_session_id.
    #
    # Dashboard can still display the session
    # that just finished.
    #
    # When Start is pressed again, a new session
    # will automatically replace it.
    # --------------------------------------------

    return {
        "message": "Live capture stopped successfully",
        "session_id": stopped_session_id
    }


# ============================================
# LIVE CAPTURE STATUS
# ============================================

@router.get("/status")
def get_live_capture_status(
    current_user=Depends(get_current_user)
):

    # --------------------------------------------
    # Running
    # --------------------------------------------

    if capture_thread and capture_thread.is_alive():

        # Another user's session
        if current_user_id != current_user.id:

            return {
                "status": "stopped",
                "message": "No active monitoring session for this user.",
                "session_id": None
            }

        return {
            "status": "running",
            "message": "Live capture is currently running",
            "session_id": current_session_id
        }

    # --------------------------------------------
    # Capture stopped
    # --------------------------------------------

    if current_user_id == current_user.id:

        return {
            "status": "stopped",
            "message": "Live capture is currently stopped",
            "session_id": current_session_id
        }

    return {
        "status": "stopped",
        "message": "No monitoring session available.",
        "session_id": None
    }