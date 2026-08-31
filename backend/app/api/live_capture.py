from fastapi import APIRouter
from threading import Thread

from app.services.live_capture import start_capture, stop_capture


# ============================================
# ROUTER
# ============================================

router = APIRouter(
    prefix="/live-capture",
    tags=["Live Capture"]
)


# ============================================
# GLOBAL CAPTURE THREAD
# ============================================

capture_thread = None


# ============================================
# START LIVE CAPTURE
# ============================================

@router.post("/start")
def start_live_capture():

    global capture_thread

    # Check if capture is already running
    if capture_thread and capture_thread.is_alive():

        return {
            "message": "Live capture is already running"
        }

    # Create background thread for packet capture
    capture_thread = Thread(
        target=start_capture,
        kwargs={
            "interface": None,
            "timeout": None
        },
        daemon=True
    )

    # Start packet capture
    capture_thread.start()

    return {
        "message": "Live capture started successfully"
    }


# ============================================
# STOP LIVE CAPTURE
# ============================================

@router.post("/stop")
def stop_live_capture():

    global capture_thread

    # Check whether capture is running
    if not capture_thread or not capture_thread.is_alive():

        return {
            "message": "Live capture is not running"
        }

    # Stop the capture service
    stop_capture()

    return {
        "message": "Live capture stopped successfully"
    }


# ============================================
# CHECK LIVE CAPTURE STATUS
# ============================================

@router.get("/status")
def get_live_capture_status():

    if capture_thread and capture_thread.is_alive():

        return {
            "status": "running",
            "message": "Live capture is currently running"
        }

    return {
        "status": "stopped",
        "message": "Live capture is currently stopped"
    }