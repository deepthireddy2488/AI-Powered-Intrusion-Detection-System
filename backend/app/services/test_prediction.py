from app.services.flow_features import calculate_basic_features
from app.services.prediction import predict_attack

from datetime import datetime, timedelta


now = datetime.now()


# Test flow
test_flow = {

    "destination_port": 443,

    "fwd_packets": 5,
    "bwd_packets": 3,

    "fwd_bytes": 1000,
    "bwd_bytes": 700,

    "fwd_lengths": [
        100, 200, 150, 250, 300
    ],

    "bwd_lengths": [
        180, 220, 160
    ],

    "packet_lengths": [
        100, 200, 150, 250,
        300, 180, 220, 160
    ],

    "fwd_header_lengths": [
        20, 20, 20, 20, 20
    ],

    "bwd_header_lengths": [
        20, 20, 20
    ],

    "start_time": now,

    "last_time":
        now + timedelta(seconds=2),

    "all_times": [
        now,
        now + timedelta(seconds=0.2),
        now + timedelta(seconds=0.5),
        now + timedelta(seconds=0.8),
        now + timedelta(seconds=1.0),
        now + timedelta(seconds=1.2),
        now + timedelta(seconds=1.6),
        now + timedelta(seconds=2.0)
    ],

    "fwd_times": [
        now,
        now + timedelta(seconds=0.5),
        now + timedelta(seconds=1.0),
        now + timedelta(seconds=1.5),
        now + timedelta(seconds=2.0)
    ],

    "bwd_times": [
        now,
        now + timedelta(seconds=0.4),
        now + timedelta(seconds=1.0)
    ],

    "fwd_psh_count": 1,
    "bwd_psh_count": 1,

    "fwd_urg_count": 0,
    "bwd_urg_count": 0,

    "fin_count": 1,
    "syn_count": 1,
    "rst_count": 0,
    "psh_count": 2,
    "ack_count": 4,
    "urg_count": 0,

    "cwe_count": 0,
    "ece_count": 0,

    "fwd_window": 65535,
    "bwd_window": 65535,

    "active_times": [],
    "idle_times": []
}


# Generate 78 features
features = calculate_basic_features(test_flow)


print()
print("==============================")
print("AI IDS PREDICTION TEST")
print("==============================")

print(
    "Generated Features:",
    len(features)
)


# Predict attack
prediction = predict_attack(features)


print(
    "Prediction:",
    prediction
)