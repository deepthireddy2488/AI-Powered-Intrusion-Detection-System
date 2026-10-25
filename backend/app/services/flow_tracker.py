from collections import defaultdict


class FlowTracker:

    def __init__(self):

        self.flows = defaultdict(lambda: {

            # ============================================
            # TIME
            # ============================================

            "start_time": None,
            "last_time": None,

            # ============================================
            # PACKETS
            # ============================================

            "fwd_packets": 0,
            "bwd_packets": 0,

            "fwd_bytes": 0,
            "bwd_bytes": 0,

            "fwd_lengths": [],
            "bwd_lengths": [],
            "packet_lengths": [],

            "fwd_times": [],
            "bwd_times": [],
            "all_times": [],

            # ============================================
            # TCP FLAGS
            # ============================================

            "syn_count": 0,
            "fin_count": 0,
            "rst_count": 0,
            "psh_count": 0,
            "ack_count": 0,
            "urg_count": 0,

            "fwd_psh_count": 0,
            "bwd_psh_count": 0,

            "fwd_urg_count": 0,
            "bwd_urg_count": 0,

            # ============================================
            # HEADER INFORMATION
            # ============================================

            "fwd_header_lengths": [],
            "bwd_header_lengths": [],

            # ============================================
            # TCP WINDOW
            # ============================================

            "fwd_window": 0,
            "bwd_window": 0,

            # ============================================
            # SEGMENT INFORMATION
            # ============================================

            "fwd_seg_sizes": [],
            "bwd_seg_sizes": [],

            # ============================================
            # ACTIVE / IDLE
            # ============================================

            "active_times": [],
            "idle_times": [],

            # ============================================
            # BULK INFORMATION
            # ============================================

            "fwd_bulk_bytes": 0,
            "fwd_bulk_packets": 0,

            "bwd_bulk_bytes": 0,
            "bwd_bulk_packets": 0,

            # ============================================
            # DATA PACKETS
            # ============================================

            "act_data_pkt_fwd": 0,

            # ============================================
            # TCP MINIMUM SEGMENT SIZE
            # ============================================

            "min_seg_size_forward": 0,

            # ============================================
            # CWE / ECE FLAGS
            # ============================================

            "cwe_count": 0,
            "ece_count": 0

        })


    # ====================================================
    # FLOW KEY
    # ====================================================

    def get_flow_key(
        self,
        src_ip,
        src_port,
        dst_ip,
        dst_port,
        protocol
    ):

        forward = (
            src_ip,
            src_port,
            dst_ip,
            dst_port,
            protocol
        )

        backward = (
            dst_ip,
            dst_port,
            src_ip,
            src_port,
            protocol
        )

        return min(forward, backward)


    # ====================================================
    # ADD PACKET
    # ====================================================

    def add_packet(
        self,
        src_ip,
        src_port,
        dst_ip,
        dst_port,
        protocol,
        packet_length,
        timestamp,
        direction,
        flags=None,
        header_length=0,
        window_size=0,
        payload_length=0
    ):

        # --------------------------------------------
        # GET FLOW KEY
        # --------------------------------------------

        key = self.get_flow_key(
            src_ip,
            src_port,
            dst_ip,
            dst_port,
            protocol
        )

        flow = self.flows[key]

        # --------------------------------------------
        # FIRST PACKET
        # --------------------------------------------

        if flow["start_time"] is None:

            flow["start_time"] = timestamp

        # --------------------------------------------
        # LAST PACKET
        # --------------------------------------------

        flow["last_time"] = timestamp

        # --------------------------------------------
        # ALL TIMES
        # --------------------------------------------

        flow["all_times"].append(timestamp)

        # --------------------------------------------
        # PACKET LENGTH
        # --------------------------------------------

        flow["packet_lengths"].append(
            packet_length
        )

        # =================================================
        # FORWARD PACKET
        # =================================================

        if direction == "forward":

            flow["fwd_packets"] += 1

            flow["fwd_bytes"] += packet_length

            flow["fwd_lengths"].append(
                packet_length
            )

            flow["fwd_times"].append(
                timestamp
            )

            # --------------------------------------------
            # HEADER
            # --------------------------------------------

            flow["fwd_header_lengths"].append(
                header_length
            )

            # --------------------------------------------
            # SEGMENT SIZE
            # --------------------------------------------

            flow["fwd_seg_sizes"].append(
                payload_length
            )

            # --------------------------------------------
            # DATA PACKET
            # --------------------------------------------

            if payload_length > 0:

                flow["act_data_pkt_fwd"] += 1

            # --------------------------------------------
            # MIN SEGMENT SIZE
            # --------------------------------------------

            if flow["min_seg_size_forward"] == 0:

                flow["min_seg_size_forward"] = (
                    header_length
                )

            else:

                flow["min_seg_size_forward"] = min(
                    flow["min_seg_size_forward"],
                    header_length
                )

            # --------------------------------------------
            # TCP WINDOW
            # --------------------------------------------

            if window_size > 0:

                flow["fwd_window"] = window_size

            # --------------------------------------------
            # BULK
            # --------------------------------------------

            if payload_length > 0:

                flow["fwd_bulk_bytes"] += payload_length

                flow["fwd_bulk_packets"] += 1

        # =================================================
        # BACKWARD PACKET
        # =================================================

        else:

            flow["bwd_packets"] += 1

            flow["bwd_bytes"] += packet_length

            flow["bwd_lengths"].append(
                packet_length
            )

            flow["bwd_times"].append(
                timestamp
            )

            # --------------------------------------------
            # HEADER
            # --------------------------------------------

            flow["bwd_header_lengths"].append(
                header_length
            )

            # --------------------------------------------
            # SEGMENT SIZE
            # --------------------------------------------

            flow["bwd_seg_sizes"].append(
                payload_length
            )

            # --------------------------------------------
            # TCP WINDOW
            # --------------------------------------------

            if window_size > 0:

                flow["bwd_window"] = window_size

            # --------------------------------------------
            # BULK
            # --------------------------------------------

            if payload_length > 0:

                flow["bwd_bulk_bytes"] += payload_length

                flow["bwd_bulk_packets"] += 1

        # =================================================
        # TCP FLAGS
        # =================================================

        if flags:

            # --------------------------------------------
            # SYN
            # --------------------------------------------

            if "S" in flags:

                flow["syn_count"] += 1

            # --------------------------------------------
            # FIN
            # --------------------------------------------

            if "F" in flags:

                flow["fin_count"] += 1

            # --------------------------------------------
            # RST
            # --------------------------------------------

            if "R" in flags:

                flow["rst_count"] += 1

            # --------------------------------------------
            # PSH
            # --------------------------------------------

            if "P" in flags:

                flow["psh_count"] += 1

                if direction == "forward":

                    flow["fwd_psh_count"] += 1

                else:

                    flow["bwd_psh_count"] += 1

            # --------------------------------------------
            # ACK
            # --------------------------------------------

            if "A" in flags:

                flow["ack_count"] += 1

            # --------------------------------------------
            # URG
            # --------------------------------------------

            if "U" in flags:

                flow["urg_count"] += 1

                if direction == "forward":

                    flow["fwd_urg_count"] += 1

                else:

                    flow["bwd_urg_count"] += 1

            # --------------------------------------------
            # CWE
            # --------------------------------------------

            if "C" in flags:

                flow["cwe_count"] += 1

            # --------------------------------------------
            # ECE
            # --------------------------------------------

            if "E" in flags:

                flow["ece_count"] += 1


    # ====================================================
    # GET ONE FLOW
    # ====================================================

    def get_flow(self, key):

        return self.flows.get(key)


    # ====================================================
    # GET ALL FLOWS
    # ====================================================

    def get_all_flows(self):

        return self.flows
    # ====================================================
    # FLOW LIFECYCLE MANAGEMENT
    # ====================================================

    def remove_flow(self, key):
        """Remove a flow and its accumulated packet statistics, if present."""
        self.flows.pop(key, None)

    def clear(self):
        """Discard every flow. Called between monitoring sessions."""
        self.flows.clear()

    def expire_stale_flows(
        self,
        now=None,
        idle_timeout_seconds=60,
        max_age_seconds=300,
    ):
        """Return and remove idle/over-age flows to bound memory use.

        A flow expires if it has been idle for `idle_timeout_seconds` or has
        exceeded `max_age_seconds`. The next packet for that 5-tuple begins a
        fresh measurement window. `now` should use the same datetime basis as
        the packet timestamps stored in this tracker.
        """
        from datetime import datetime

        now = now or datetime.now()
        expired_keys = []

        for key, flow in list(self.flows.items()):
            started = flow.get("start_time")
            last_seen = flow.get("last_time")
            if started is None or last_seen is None:
                expired_keys.append(key)
                continue

            idle_seconds = (now - last_seen).total_seconds()
            age_seconds = (now - started).total_seconds()
            if idle_seconds >= idle_timeout_seconds or age_seconds >= max_age_seconds:
                expired_keys.append(key)

        for key in expired_keys:
            self.flows.pop(key, None)

        return expired_keys
