from datetime import datetime


# ============================================
# ATTACK SEVERITY
# ============================================

SEVERITY = {

    "BENIGN": "LOW",

    "PortScan": "HIGH",

    "DDoS": "CRITICAL",

    "DoS Hulk": "CRITICAL",

    "DoS GoldenEye": "HIGH",

    "DoS Slowhttptest": "HIGH",

    "DoS slowloris": "HIGH",

    "Bot": "HIGH",

    "FTP-Patator": "HIGH",

    "SSH-Patator": "HIGH",

    "Heartbleed": "CRITICAL",

    "Infiltration": "CRITICAL",

    "Web Attack – Brute Force": "HIGH",

    "Web Attack – Sql Injection": "CRITICAL",

    "Web Attack – XSS": "HIGH"
}


# ============================================
# GET SEVERITY
# ============================================

def get_severity(attack_name):

    return SEVERITY.get(
        attack_name,
        "HIGH"
    )


# ============================================
# GENERATE ALERT
# ============================================

def generate_alert(
    attack_name,
    source_ip,
    source_port,
    destination_ip,
    destination_port,
    protocol,
    packet_count
):

    # --------------------------------
    # BENIGN TRAFFIC
    # --------------------------------

    if attack_name == "BENIGN":

        return None


    # --------------------------------
    # ATTACK DETECTED
    # --------------------------------

    severity = get_severity(
        attack_name
    )

    alert = {

        "timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "attack_type":
            attack_name,

        "severity":
            severity,

        "source_ip":
            source_ip,

        "source_port":
            source_port,

        "destination_ip":
            destination_ip,

        "destination_port":
            destination_port,

        "protocol":
            protocol,

        "packet_count":
            packet_count
    }

    return alert


# ============================================
# DISPLAY ALERT
# ============================================

def display_alert(alert):

    if alert is None:

        return


    print()

    print(
        "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    )

    print(
        "       INTRUSION DETECTED"
    )

    print(
        "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    )

    print(
        f"Time: "
        f"{alert['timestamp']}"
    )

    print(
        f"Attack Type: "
        f"{alert['attack_type']}"
    )

    print(
        f"Severity: "
        f"{alert['severity']}"
    )

    print(
        f"Source: "
        f"{alert['source_ip']}:"
        f"{alert['source_port']}"
    )

    print(
        f"Destination: "
        f"{alert['destination_ip']}:"
        f"{alert['destination_port']}"
    )

    print(
        f"Protocol: "
        f"{alert['protocol']}"
    )

    print(
        f"Packets: "
        f"{alert['packet_count']}"
    )

    print(
        "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    )

    print()