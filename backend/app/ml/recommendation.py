def get_recommendation(attack_type: str):

    recommendations = {

        "BENIGN":
        "Normal network traffic. No action required.",

        "PortScan":
        "Block suspicious IP and monitor scanning activity.",

        "DDoS":
        "Enable firewall protection and block attacking IPs.",

        "DoS Hulk":
        "Apply rate limiting and monitor traffic.",

        "DoS GoldenEye":
        "Inspect server logs and enable protection.",

        "DoS slowloris":
        "Increase timeout protection and filter requests.",

        "DoS Slowhttptest":
        "Configure web server to detect slow attacks.",

        "Bot":
        "Isolate infected devices and perform malware scan.",

        "FTP-Patator":
        "Disable repeated login attempts and change credentials.",

        "SSH-Patator":
        "Enable SSH key authentication and block IP.",

        "Web Attack – Brute Force":
        "Enable account lockout and strong passwords.",

        "Web Attack – XSS":
        "Validate user input and sanitize data.",

        "Web Attack – Sql Injection":
        "Use parameterized SQL queries and validate input.",

        "Heartbleed":
        "Update OpenSSL immediately.",

        "Infiltration":
        "Disconnect affected system and investigate immediately."
    }

    return recommendations.get(
        attack_type,
        "No recommendation available."
    )