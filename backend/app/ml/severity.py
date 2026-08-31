def get_severity(attack_type: str):

    severity = {
        "BENIGN": "Low",
        "PortScan": "Medium",
        "DDoS": "High",
        "DoS Hulk": "High",
        "DoS GoldenEye": "High",
        "DoS slowloris": "High",
        "DoS Slowhttptest": "High",
        "Bot": "High",
        "FTP-Patator": "Medium",
        "SSH-Patator": "Medium",
        "Web Attack – Brute Force": "High",
        "Web Attack – XSS": "Medium",
        "Web Attack – Sql Injection": "High",
        "Heartbleed": "Critical",
        "Infiltration": "Critical"
    }

    return severity.get(attack_type, "Unknown")