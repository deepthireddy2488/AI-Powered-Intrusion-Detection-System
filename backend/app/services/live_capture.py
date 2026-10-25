from scapy.all import AsyncSniffer, IP, TCP, UDP
from threading import RLock
from datetime import datetime

from app.services.flow_tracker import FlowTracker
from app.services.flow_features import calculate_basic_features
from app.services.prediction import predict_attack_with_confidence
from app.services.alert_service import (
    generate_alert,
    display_alert,
)
from app.ml.recommendation import get_recommendation
from app.ml.severity import get_severity
from app.database.database import SessionLocal
from app.repositories.attack_log_repository import create_attack_log


# ============================================
# GLOBAL OBJECTS
# ============================================

tracker = FlowTracker()

# Stores the original direction of each flow
flow_directions = {}

# Counts packets in each flow
flow_packet_counts = {}

# Controls whether live capture is running
capture_running = False
_sniffer = None
_stop_requested = False
_capture_lock = RLock()

# These are configurable policy values, not universal IDS thresholds.
PREDICTION_EVERY_N_PACKETS = 2
FLOW_IDLE_TIMEOUT_SECONDS = 60
FLOW_MAX_AGE_SECONDS = 300
FLOW_MAX_PACKETS = 500

# ============================================
# CURRENT USER / SESSION
# ============================================

active_user_id = None
active_session_id = None


# ============================================
# PROCESS PACKET
# ============================================

def process_packet(packet):

    global capture_running

    if not capture_running:
        return

    if IP not in packet:
        return

    ip_layer = packet[IP]

    src_ip = ip_layer.src
    dst_ip = ip_layer.dst

    # ========================================
    # TCP
    # ========================================

    if TCP in packet:

        protocol = "TCP"
        transport = packet[TCP]

        src_port = transport.sport
        dst_port = transport.dport

        flags = str(transport.flags)

        header_length = (
            transport.dataofs * 4
            if transport.dataofs
            else 20
        )

        window_size = transport.window

        payload_length = len(
            transport.payload
        )

    # ========================================
    # UDP
    # ========================================

    elif UDP in packet:

        protocol = "UDP"
        transport = packet[UDP]

        src_port = transport.sport
        dst_port = transport.dport

        flags = ""
        header_length = 8
        window_size = 0

        payload_length = len(
            transport.payload
        )

    else:
        return

    # ========================================
    # PACKET INFORMATION
    # ========================================

    packet_length = len(packet)

    timestamp = datetime.fromtimestamp(
        float(packet.time)
    )

    # Expire stale flows before looking up this packet's flow. This prevents
    # old flow statistics from being reused indefinitely during monitoring.
    expired_keys = tracker.expire_stale_flows(
        now=timestamp,
        idle_timeout_seconds=FLOW_IDLE_TIMEOUT_SECONDS,
        max_age_seconds=FLOW_MAX_AGE_SECONDS,
    )
    for expired_key in expired_keys:
        flow_directions.pop(expired_key, None)
        flow_packet_counts.pop(expired_key, None)

    # ========================================
    # FLOW KEY
    # ========================================

    flow_key = tracker.get_flow_key(
        src_ip,
        src_port,
        dst_ip,
        dst_port,
        protocol
    )

    # Bound memory for persistent high-volume flows. Once a flow window reaches
    # the configured packet cap, start a new measurement window for the same 5-tuple.
    if flow_packet_counts.get(flow_key, 0) >= FLOW_MAX_PACKETS:
        tracker.remove_flow(flow_key)
        flow_packet_counts.pop(flow_key, None)
        flow_directions.pop(flow_key, None)

    # ========================================
    # DETERMINE DIRECTION
    # ========================================

    if flow_key not in flow_directions:

        flow_directions[flow_key] = (
            src_ip,
            src_port,
            dst_ip,
            dst_port
        )

        direction = "forward"

    else:

        original = flow_directions[flow_key]

        if (
            src_ip == original[0]
            and
            src_port == original[1]
        ):

            direction = "forward"

        else:

            direction = "backward"

    # ========================================
    # ADD PACKET TO FLOW TRACKER
    # ========================================

    tracker.add_packet(

        src_ip=src_ip,

        src_port=src_port,

        dst_ip=dst_ip,

        dst_port=dst_port,

        protocol=protocol,

        packet_length=packet_length,

        timestamp=timestamp,

        direction=direction,

        flags=flags,

        header_length=header_length,

        window_size=window_size,

        payload_length=payload_length
    )

    # ========================================
    # PACKET COUNT
    # ========================================

    if flow_key not in flow_packet_counts:
        flow_packet_counts[flow_key] = 0

    flow_packet_counts[flow_key] += 1

    packet_count = flow_packet_counts[flow_key]

    # ========================================
    # DISPLAY PACKET
    # ========================================

    print(
        f"[PACKET] "
        f"{src_ip}:{src_port} -> "
        f"{dst_ip}:{dst_port} | "
        f"{protocol} | "
        f"{packet_length} bytes | "
        f"{direction}"
    )

    # ========================================
    # PREDICTION CHECKPOINT
    # ========================================

    if packet_count % PREDICTION_EVERY_N_PACKETS != 0:
        return

    print()
    print("========================================")
    print(f"  {PREDICTION_EVERY_N_PACKETS} PACKET CHECKPOINT - AI PREDICTION")
    print("========================================")

    print(
        f"Flow Key: {flow_key}"
    )

    print(
        f"Packet Count: {packet_count}"
    )

    # ========================================
    # GET FLOW
    # ========================================

    flow = tracker.get_flow(flow_key)

    if not flow:

        print(
            "ERROR: Flow not found!"
        )

        return

    print(
        "FLOW RETRIEVED SUCCESSFULLY"
    )

    # ========================================
    # ORIGINAL FLOW INFORMATION
    # ========================================

    original = flow_directions[flow_key]

    source_ip = original[0]
    source_port = original[1]

    destination_ip = original[2]
    destination_port = original[3]

    # ========================================
    # PREPARE FEATURE FLOW
    # ========================================

    feature_flow = dict(flow)

    feature_flow["dst_port"] = destination_port

    # ========================================
    # FEATURE GENERATION AND PREDICTION
    # ========================================

    try:

        print()
        print(
            "STARTING FEATURE GENERATION..."
        )

        features = calculate_basic_features(
            feature_flow
        )

        print(
            "FEATURE GENERATION COMPLETED"
        )

        print(
            f"Generated feature count: "
            f"{len(features)}"
        )

        # ====================================
        # FEATURE COUNT CHECK
        # ====================================

        if len(features) != 78:

            print()
            print("==============================")
            print("FEATURE COUNT ERROR")
            print("==============================")

            print("Expected: 78")

            print(
                f"Generated: {len(features)}"
            )

            print("==============================")

            return

        print(
            "FEATURE COUNT IS CORRECT: 78"
        )

        # ====================================
        # AI PREDICTION
        # ====================================

        print()
        print(
            "STARTING AI PREDICTION..."
        )

        prediction, confidence = predict_attack_with_confidence(
            features
        )

        print(
            "PREDICTION COMPLETED"
        )

        print(
            f"Prediction result: {prediction}"
        )

        # ====================================
        # GENERATE ALERT
        # ====================================

        print()
        print(
            "GENERATING ALERT..."
        )

        alert = generate_alert(

            attack_name=prediction,

            source_ip=source_ip,
            source_port=source_port,

            destination_ip=destination_ip,
            destination_port=destination_port,

            protocol=protocol,

            packet_count=packet_count
        )

        print(
            "ALERT GENERATED"
        )

        # ====================================
        # DISPLAY ALERT
        # ====================================

        display_alert(alert)

        # ========================================
        # SAVE RESULT TO DATABASE
        # ========================================

        db = SessionLocal()

        try:

            severity = get_severity(prediction)
            recommendation = get_recommendation(prediction)

            status = (
                "Detected"
                if prediction != "BENIGN"
                else "Normal"
            )

            # ====================================
            # IMPORTANT:
            # Save user + session ownership
            # ====================================

            if active_user_id is None:
                print(
                    "ERROR: No active user ID."
                )

                return

            if active_session_id is None:
                print(
                    "ERROR: No active session ID."
                )

                return

            create_attack_log(

                db=db,

                source_ip=source_ip,

                destination_ip=destination_ip,

                attack_type=prediction,

                severity=severity,

                status=status,

                source_port=source_port,
                destination_port=destination_port,
                protocol=protocol,
                packet_count=packet_count,
                confidence=confidence,
                recommendation=recommendation,

                user_id=active_user_id,

                session_id=active_session_id
            )

            print(
                "ATTACK LOG SAVED TO DATABASE"
            )

            print(
                f"User ID: {active_user_id}"
            )

            print(
                f"Session ID: {active_session_id}"
            )

        except Exception as error:

            print(
                f"ERROR SAVING ATTACK LOG: {error}"
            )

        finally:

            db.close()

        # ====================================
        # FINAL RESULT
        # ====================================

        print()

        print("===================================")
        print("      AI IDS LIVE PREDICTION")
        print("===================================")

        print(
            f"Flow: "
            f"{source_ip}:{source_port} -> "
            f"{destination_ip}:{destination_port}"
        )

        print(
            f"Protocol: {protocol}"
        )

        print(
            f"Packets: {packet_count}"
        )

        print(
            f"Generated Features: {len(features)}"
        )

        print(
            f"Prediction: {prediction}"
        )

        print("===================================")
        print()

    # ========================================
    # ERROR HANDLING
    # ========================================

    except Exception as error:

        print()

        print("===================================")
        print("       PREDICTION ERROR")
        print("===================================")

        print(
            f"Error Type: "
            f"{type(error).__name__}"
        )

        print(
            f"Error Message: {error}"
        )

        print("===================================")
        print()


# ============================================
# START LIVE CAPTURE
# ============================================

def start_capture(
    interface=None,
    timeout=None,
    user_id=None,
    session_id=None
):
    """Start one Scapy capture and keep the worker alive until it stops."""
    global capture_running
    global active_user_id
    global active_session_id
    global tracker
    global flow_directions
    global flow_packet_counts
    global _sniffer
    global _stop_requested

    with _capture_lock:
        # A stop can arrive immediately after the API creates the worker thread,
        # before this function has initialized the sniffer. Honor that request
        # instead of accidentally starting a capture after the user stopped it.
        if _stop_requested:
            _stop_requested = False
            print("Capture start cancelled by an early stop request.")
            return

        if capture_running:
            print("Live capture is already running.")
            return

        # Fresh state per session: previous traffic must never leak into a new run.
        tracker = FlowTracker()
        flow_directions = {}
        flow_packet_counts = {}
        active_user_id = user_id
        active_session_id = session_id
        capture_running = True

        sniffer = AsyncSniffer(
            iface=interface,
            prn=process_packet,
            store=False,
            timeout=timeout,
        )
        _sniffer = sniffer

    print("\n===================================")
    print("     AI IDS LIVE PACKET CAPTURE")
    print("===================================")
    print(f"User ID: {user_id}")
    print(f"Session ID: {session_id}")
    print(f"Interface: {interface or 'Default'}")
    print("Capturing TCP/UDP packets...")
    print(f"Prediction checkpoint: every {PREDICTION_EVERY_N_PACKETS} packets per flow window")
    print(f"Idle flow expiry: {FLOW_IDLE_TIMEOUT_SECONDS}s; maximum window age: {FLOW_MAX_AGE_SECONDS}s")

    try:
        sniffer.start()
        # Handle a stop request that races with the sniffer's startup.
        with _capture_lock:
            stop_requested = _stop_requested
        if stop_requested and getattr(sniffer, "running", False):
            sniffer.stop(join=True)
        # The API starts this function in a worker thread. join() keeps that
        # worker alive for /status and lets stop_capture() wait for a real stop.
        sniffer.join()
    except Exception as error:
        print(f"LIVE CAPTURE ERROR ({type(error).__name__}): {error}")
    finally:
        with _capture_lock:
            capture_running = False
            _stop_requested = False
            active_user_id = None
            active_session_id = None
            flow_directions.clear()
            flow_packet_counts.clear()
            tracker.clear()
            if _sniffer is sniffer:
                _sniffer = None
        print("Live packet capture stopped and session state cleared.")


def stop_capture():
    """Stop capture synchronously, including when no new packets arrive."""
    global capture_running
    global _stop_requested

    with _capture_lock:
        sniffer = _sniffer
        was_running = capture_running
        _stop_requested = True
        capture_running = False

    if sniffer is not None:
        try:
            if getattr(sniffer, "running", False):
                sniffer.stop(join=True)
        except Exception as error:
            # A packet timeout or capture failure may have already stopped it.
            print(f"Capture stop notice: {error}")

    if not was_running:
        return {"message": "Live capture is not running"}

    print("Stop request completed; packet-capture worker joined.")
    return {"message": "Live capture stopped successfully"}


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    start_capture()