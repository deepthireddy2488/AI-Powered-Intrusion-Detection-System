import statistics


# ============================================================
# SAFE STATISTICS
# ============================================================

def safe_mean(values):
    if not values:
        return 0.0

    return sum(values) / len(values)


def safe_std(values):
    if len(values) < 2:
        return 0.0

    return statistics.stdev(values)


def safe_variance(values):
    if len(values) < 2:
        return 0.0

    return statistics.variance(values)


def safe_min(values):
    if not values:
        return 0.0

    return min(values)


def safe_max(values):
    if not values:
        return 0.0

    return max(values)


# ============================================================
# IAT CALCULATION
# ============================================================

def get_iat_values(times):

    if len(times) < 2:
        return []

    values = []

    for i in range(1, len(times)):

        difference = (
            times[i] - times[i - 1]
        ).total_seconds() * 1_000_000

        values.append(difference)

    return values


# ============================================================
# MAIN FEATURE GENERATION
# ============================================================

def calculate_basic_features(flow):

    # ========================================================
    # BASIC FLOW DATA
    # ========================================================

    fwd_packets = flow.get(
        "fwd_packets",
        0
    )

    bwd_packets = flow.get(
        "bwd_packets",
        0
    )

    fwd_bytes = flow.get(
        "fwd_bytes",
        0
    )

    bwd_bytes = flow.get(
        "bwd_bytes",
        0
    )

    packet_lengths = flow.get(
        "packet_lengths",
        []
    )

    fwd_lengths = flow.get(
        "fwd_lengths",
        []
    )

    bwd_lengths = flow.get(
        "bwd_lengths",
        []
    )

    # ========================================================
    # TIME INFORMATION
    # ========================================================

    start_time = flow.get(
        "start_time"
    )

    last_time = flow.get(
        "last_time"
    )

    if start_time is not None and last_time is not None:

        duration = (
            last_time - start_time
        ).total_seconds() * 1_000_000

    else:

        duration = 0.0


    # Prevent negative duration
    if duration < 0:
        duration = 0.0


    # ========================================================
    # TOTALS
    # ========================================================

    total_packets = (
        fwd_packets +
        bwd_packets
    )

    total_bytes = (
        fwd_bytes +
        bwd_bytes
    )


    # ========================================================
    # FLOW RATES
    # ========================================================

    if duration > 0:

        duration_seconds = (
            duration / 1_000_000
        )

        flow_bytes_per_second = (
            total_bytes /
            duration_seconds
        )

        flow_packets_per_second = (
            total_packets /
            duration_seconds
        )

        fwd_packets_per_second = (
            fwd_packets /
            duration_seconds
        )

        bwd_packets_per_second = (
            bwd_packets /
            duration_seconds
        )

    else:

        flow_bytes_per_second = 0.0
        flow_packets_per_second = 0.0
        fwd_packets_per_second = 0.0
        bwd_packets_per_second = 0.0


    # ========================================================
    # TIMES
    # ========================================================

    all_times = flow.get(
        "all_times",
        []
    )

    fwd_times = flow.get(
        "fwd_times",
        []
    )

    bwd_times = flow.get(
        "bwd_times",
        []
    )


    # ========================================================
    # IAT
    # ========================================================

    flow_iat = get_iat_values(
        all_times
    )

    fwd_iat = get_iat_values(
        fwd_times
    )

    bwd_iat = get_iat_values(
        bwd_times
    )


    # ========================================================
    # FLOW IAT
    # ========================================================

    flow_iat_mean = safe_mean(
        flow_iat
    )

    flow_iat_std = safe_std(
        flow_iat
    )

    flow_iat_max = safe_max(
        flow_iat
    )

    flow_iat_min = safe_min(
        flow_iat
    )


    # ========================================================
    # FORWARD IAT
    # ========================================================

    fwd_iat_total = sum(
        fwd_iat
    )

    fwd_iat_mean = safe_mean(
        fwd_iat
    )

    fwd_iat_std = safe_std(
        fwd_iat
    )

    fwd_iat_max = safe_max(
        fwd_iat
    )

    fwd_iat_min = safe_min(
        fwd_iat
    )


    # ========================================================
    # BACKWARD IAT
    # ========================================================

    bwd_iat_total = sum(
        bwd_iat
    )

    bwd_iat_mean = safe_mean(
        bwd_iat
    )

    bwd_iat_std = safe_std(
        bwd_iat
    )

    bwd_iat_max = safe_max(
        bwd_iat
    )

    bwd_iat_min = safe_min(
        bwd_iat
    )


    # ========================================================
    # FORWARD PACKET LENGTHS
    # ========================================================

    fwd_packet_max = safe_max(
        fwd_lengths
    )

    fwd_packet_min = safe_min(
        fwd_lengths
    )

    fwd_packet_mean = safe_mean(
        fwd_lengths
    )

    fwd_packet_std = safe_std(
        fwd_lengths
    )


    # ========================================================
    # BACKWARD PACKET LENGTHS
    # ========================================================

    bwd_packet_max = safe_max(
        bwd_lengths
    )

    bwd_packet_min = safe_min(
        bwd_lengths
    )

    bwd_packet_mean = safe_mean(
        bwd_lengths
    )

    bwd_packet_std = safe_std(
        bwd_lengths
    )


    # ========================================================
    # ALL PACKET LENGTHS
    # ========================================================

    packet_min = safe_min(
        packet_lengths
    )

    packet_max = safe_max(
        packet_lengths
    )

    packet_mean = safe_mean(
        packet_lengths
    )

    packet_std = safe_std(
        packet_lengths
    )

    packet_variance = safe_variance(
        packet_lengths
    )


    # ========================================================
    # HEADER LENGTHS
    # ========================================================

    fwd_header_lengths = flow.get(
        "fwd_header_lengths",
        []
    )

    bwd_header_lengths = flow.get(
        "bwd_header_lengths",
        []
    )

    fwd_header_length = sum(
        fwd_header_lengths
    )

    bwd_header_length = sum(
        bwd_header_lengths
    )


    # ========================================================
    # FLAGS
    # ========================================================

    fin_count = flow.get(
        "fin_count",
        0
    )

    syn_count = flow.get(
        "syn_count",
        0
    )

    rst_count = flow.get(
        "rst_count",
        0
    )

    psh_count = flow.get(
        "psh_count",
        0
    )

    ack_count = flow.get(
        "ack_count",
        0
    )

    urg_count = flow.get(
        "urg_count",
        0
    )

    fwd_psh_count = flow.get(
        "fwd_psh_count",
        0
    )

    bwd_psh_count = flow.get(
        "bwd_psh_count",
        0
    )

    fwd_urg_count = flow.get(
        "fwd_urg_count",
        0
    )

    bwd_urg_count = flow.get(
        "bwd_urg_count",
        0
    )

    cwe_count = flow.get(
        "cwe_count",
        0
    )

    ece_count = flow.get(
        "ece_count",
        0
    )


    # ========================================================
    # DOWN / UP RATIO
    # ========================================================

    if fwd_packets > 0:

        down_up_ratio = (
            bwd_packets /
            fwd_packets
        )

    else:

        down_up_ratio = 0.0


    # ========================================================
    # AVERAGE PACKET SIZE
    # ========================================================

    average_packet_size = (
        safe_mean(packet_lengths)
    )

    avg_fwd_segment_size = (
        safe_mean(fwd_lengths)
    )

    avg_bwd_segment_size = (
        safe_mean(bwd_lengths)
    )


    # ========================================================
    # WINDOW SIZE
    # ========================================================

    fwd_window = flow.get(
        "fwd_window",
        0
    )

    bwd_window = flow.get(
        "bwd_window",
        0
    )


    # ========================================================
    # ACTIVE / IDLE
    # ========================================================

    active_times = flow.get(
        "active_times",
        []
    )

    idle_times = flow.get(
        "idle_times",
        []
    )


    active_mean = safe_mean(
        active_times
    )

    active_std = safe_std(
        active_times
    )

    active_max = safe_max(
        active_times
    )

    active_min = safe_min(
        active_times
    )


    idle_mean = safe_mean(
        idle_times
    )

    idle_std = safe_std(
        idle_times
    )

    idle_max = safe_max(
        idle_times
    )

    idle_min = safe_min(
        idle_times
    )


    # ========================================================
    # MINIMUM SEGMENT SIZE
    # ========================================================

    min_seg_size_forward = flow.get(
        "min_seg_size_forward",
        safe_min(fwd_lengths)
    )


    # ========================================================
    # ACTIVE DATA PACKETS FORWARD
    # ========================================================

    act_data_pkt_fwd = flow.get(
        "act_data_pkt_fwd",
        max(fwd_packets - 1, 0)
    )


    # ========================================================
    # BULK FEATURES
    # ========================================================
    # These require additional TCP bulk-flow tracking.
    # Until that tracking is implemented, use zero.
    # ========================================================

    fwd_avg_bytes_bulk = flow.get(
        "fwd_avg_bytes_bulk",
        0.0
    )

    fwd_avg_packets_bulk = flow.get(
        "fwd_avg_packets_bulk",
        0.0
    )

    fwd_avg_bulk_rate = flow.get(
        "fwd_avg_bulk_rate",
        0.0
    )

    bwd_avg_bytes_bulk = flow.get(
        "bwd_avg_bytes_bulk",
        0.0
    )

    bwd_avg_packets_bulk = flow.get(
        "bwd_avg_packets_bulk",
        0.0
    )

    bwd_avg_bulk_rate = flow.get(
        "bwd_avg_bulk_rate",
        0.0
    )


    # ========================================================
    # SUBFLOW
    # ========================================================

    subflow_fwd_packets = flow.get(
        "subflow_fwd_packets",
        fwd_packets
    )

    subflow_fwd_bytes = flow.get(
        "subflow_fwd_bytes",
        fwd_bytes
    )

    subflow_bwd_packets = flow.get(
        "subflow_bwd_packets",
        bwd_packets
    )

    subflow_bwd_bytes = flow.get(
        "subflow_bwd_bytes",
        bwd_bytes
    )


    # ========================================================
    # 78 MODEL FEATURES
    # ========================================================

    features = {

        # 1
        "Destination Port":
            flow.get("dst_port", 0),

        # 2
        "Flow Duration":
            duration,

        # 3
        "Total Fwd Packets":
            fwd_packets,

        # 4
        "Total Backward Packets":
            bwd_packets,

        # 5
        "Total Length of Fwd Packets":
            fwd_bytes,

        # 6
        "Total Length of Bwd Packets":
            bwd_bytes,

        # 7
        "Fwd Packet Length Max":
            fwd_packet_max,

        # 8
        "Fwd Packet Length Min":
            fwd_packet_min,

        # 9
        "Fwd Packet Length Mean":
            fwd_packet_mean,

        # 10
        "Fwd Packet Length Std":
            fwd_packet_std,

        # 11
        "Bwd Packet Length Max":
            bwd_packet_max,

        # 12
        "Bwd Packet Length Min":
            bwd_packet_min,

        # 13
        "Bwd Packet Length Mean":
            bwd_packet_mean,

        # 14
        "Bwd Packet Length Std":
            bwd_packet_std,

        # 15
        "Flow Bytes/s":
            flow_bytes_per_second,

        # 16
        "Flow Packets/s":
            flow_packets_per_second,

        # 17
        "Flow IAT Mean":
            flow_iat_mean,

        # 18
        "Flow IAT Std":
            flow_iat_std,

        # 19
        "Flow IAT Max":
            flow_iat_max,

        # 20
        "Flow IAT Min":
            flow_iat_min,

        # 21
        "Fwd IAT Total":
            fwd_iat_total,

        # 22
        "Fwd IAT Mean":
            fwd_iat_mean,

        # 23
        "Fwd IAT Std":
            fwd_iat_std,

        # 24
        "Fwd IAT Max":
            fwd_iat_max,

        # 25
        "Fwd IAT Min":
            fwd_iat_min,

        # 26
        "Bwd IAT Total":
            bwd_iat_total,

        # 27
        "Bwd IAT Mean":
            bwd_iat_mean,

        # 28
        "Bwd IAT Std":
            bwd_iat_std,

        # 29
        "Bwd IAT Max":
            bwd_iat_max,

        # 30
        "Bwd IAT Min":
            bwd_iat_min,

        # 31
        "Fwd PSH Flags":
            fwd_psh_count,

        # 32
        "Bwd PSH Flags":
            bwd_psh_count,

        # 33
        "Fwd URG Flags":
            fwd_urg_count,

        # 34
        "Bwd URG Flags":
            bwd_urg_count,

        # 35
        "Fwd Header Length":
            fwd_header_length,

        # 36
        "Bwd Header Length":
            bwd_header_length,

        # 37
        "Fwd Packets/s":
            fwd_packets_per_second,

        # 38
        "Bwd Packets/s":
            bwd_packets_per_second,

        # 39
        "Min Packet Length":
            packet_min,

        # 40
        "Max Packet Length":
            packet_max,

        # 41
        "Packet Length Mean":
            packet_mean,

        # 42
        "Packet Length Std":
            packet_std,

        # 43
        "Packet Length Variance":
            packet_variance,

        # 44
        "FIN Flag Count":
            fin_count,

        # 45
        "SYN Flag Count":
            syn_count,

        # 46
        "RST Flag Count":
            rst_count,

        # 47
        "PSH Flag Count":
            psh_count,

        # 48
        "ACK Flag Count":
            ack_count,

        # 49
        "URG Flag Count":
            urg_count,

        # 50
        "CWE Flag Count":
            cwe_count,

        # 51
        "ECE Flag Count":
            ece_count,

        # 52
        "Down/Up Ratio":
            down_up_ratio,

        # 53
        "Average Packet Size":
            average_packet_size,

        # 54
        "Avg Fwd Segment Size":
            avg_fwd_segment_size,

        # 55
        "Avg Bwd Segment Size":
            avg_bwd_segment_size,

        # 56
        "Fwd Header Length.1":
            fwd_header_length,

        # 57
        "Fwd Avg Bytes/Bulk":
            fwd_avg_bytes_bulk,

        # 58
        "Fwd Avg Packets/Bulk":
            fwd_avg_packets_bulk,

        # 59
        "Fwd Avg Bulk Rate":
            fwd_avg_bulk_rate,

        # 60
        "Bwd Avg Bytes/Bulk":
            bwd_avg_bytes_bulk,

        # 61
        "Bwd Avg Packets/Bulk":
            bwd_avg_packets_bulk,

        # 62
        "Bwd Avg Bulk Rate":
            bwd_avg_bulk_rate,

        # 63
        "Subflow Fwd Packets":
            subflow_fwd_packets,

        # 64
        "Subflow Fwd Bytes":
            subflow_fwd_bytes,

        # 65
        "Subflow Bwd Packets":
            subflow_bwd_packets,

        # 66
        "Subflow Bwd Bytes":
            subflow_bwd_bytes,

        # 67
        "Init_Win_bytes_forward":
            fwd_window,

        # 68
        "Init_Win_bytes_backward":
            bwd_window,

        # 69
        "act_data_pkt_fwd":
            act_data_pkt_fwd,

        # 70
        "min_seg_size_forward":
            min_seg_size_forward,

        # 71
        "Active Mean":
            active_mean,

        # 72
        "Active Std":
            active_std,

        # 73
        "Active Max":
            active_max,

        # 74
        "Active Min":
            active_min,

        # 75
        "Idle Mean":
            idle_mean,

        # 76
        "Idle Std":
            idle_std,

        # 77
        "Idle Max":
            idle_max,

        # 78
        "Idle Min":
            idle_min
    }


    # ========================================================
    # FINAL SAFETY CHECK
    # ========================================================

    if len(features) != 78:

        raise ValueError(
            f"Feature generation failed. "
            f"Expected 78, generated {len(features)}."
        )


    return features