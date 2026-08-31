from scapy.all import sniff, IP, TCP, UDP
from datetime import datetime

from app.services.flow_tracker import FlowTracker
from app.services.flow_features import calculate_basic_features
from app.services.prediction import predict_attack
from app.services.alert_service import (
    generate_alert,
    display_alert
)
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


# ============================================
# PROCESS PACKET
# ============================================

def process_packet(packet):

    global capture_running

    # Stop processing if capture was stopped
    if not capture_running:
        return

    # ----------------------------------------
    # Ignore packets without IP
    # ----------------------------------------

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
    # PREDICTION EVERY 5 PACKETS
    # ========================================

    if packet_count % 5 != 0:
        return


    print()
    print("========================================")
    print("  5 PACKETS REACHED - AI PREDICTION")
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

    flow = tracker.get_flow(
        flow_key
    )

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

    original = flow_directions[
        flow_key
    ]

    source_ip = original[0]
    source_port = original[1]

    destination_ip = original[2]
    destination_port = original[3]


    # ========================================
    # PREPARE FEATURE FLOW
    # ========================================

    feature_flow = dict(flow)

    feature_flow["dst_port"] = (
        destination_port
    )


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


        prediction = predict_attack(
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

        display_alert(
            alert
        )


        # ========================================
        # SAVE RESULT TO DATABASE
        # ========================================

        db = SessionLocal()

        try:

            severity = (
                alert["severity"]
                if alert is not None
                else "Low"
            )

            status = (
                "Detected"
                if prediction != "BENIGN"
                else "Normal"
            )


            create_attack_log(

                db=db,

                source_ip=source_ip,

                destination_ip=destination_ip,

                attack_type=prediction,

                severity=severity,

                status=status
            )


            print(
                "ATTACK LOG SAVED TO DATABASE"
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
    timeout=None
):

    global capture_running

    # Do not start twice
    if capture_running:

        print(
            "Live capture is already running."
        )

        return


    capture_running = True


    print()

    print("===================================")
    print("     AI IDS LIVE PACKET CAPTURE")
    print("===================================")


    if interface:

        print(
            f"Interface: {interface}"
        )

    else:

        print(
            "Interface: Default"
        )


    print(
        "Capturing real packets..."
    )

    print(
        "Prediction every 5 packets "
        "per flow."
    )

    print(
        "Use the Stop API endpoint to stop."
    )

    print()


    try:

        # timeout=None means continuous capture
        # stop_filter checks capture_running
        sniff(

            iface=interface,

            prn=process_packet,

            store=False,

            timeout=timeout,

            stop_filter=lambda packet: not capture_running
        )


    except KeyboardInterrupt:

        print()

        print(
            "Capture stopped by user."
        )


    except Exception as error:

        print()

        print("===================================")
        print("        CAPTURE ERROR")
        print("===================================")

        print(
            f"Error Type: "
            f"{type(error).__name__}"
        )

        print(
            f"Error Message: {error}"
        )

        print("===================================")


    finally:

        capture_running = False

        print(
            "Live packet capture stopped."
        )


# ============================================
# STOP LIVE CAPTURE
# ============================================

def stop_capture():

    global capture_running

    if not capture_running:

        return {
            "message": "Live capture is not running"
        }


    capture_running = False


    print()

    print("===================================")
    print("      STOPPING LIVE CAPTURE")
    print("===================================")

    print(
        "Stop request received."
    )

    print(
        "Waiting for packet capture to stop..."
    )

    print("===================================")

    return {
        "message": "Live capture stop request sent"
    }


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    start_capture()