from app.services.alert_service import (
    generate_alert,
    display_alert
)


alert = generate_alert(

    attack_name="PortScan",

    source_ip="192.168.1.10",

    source_port=5000,

    destination_ip="192.168.1.20",

    destination_port=443,

    protocol="TCP",

    packet_count=25
)


display_alert(alert)