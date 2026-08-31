from datetime import datetime
from scapy.all import sniff, IP, TCP, UDP

from .flow_tracker import FlowTracker


class PacketCapture:

    def __init__(self):

        # Flow tracker
        self.flow_tracker = FlowTracker()

        # Store the original direction of each flow
        self.flow_directions = {}

        # Capture status
        self.running = False


    # =========================================================
    # GET FLOW KEY
    # =========================================================

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


    # =========================================================
    # GET PACKET INFORMATION
    # =========================================================

    def process_packet(self, packet):

        # -----------------------------------------------------
        # We only process IP packets
        # -----------------------------------------------------

        if not packet.haslayer(IP):
            return


        ip_layer = packet[IP]

        src_ip = ip_layer.src
        dst_ip = ip_layer.dst


        # -----------------------------------------------------
        # Determine protocol
        # -----------------------------------------------------

        if packet.haslayer(TCP):

            protocol = "TCP"

            transport = packet[TCP]

            src_port = transport.sport
            dst_port = transport.dport

            flags = str(transport.flags)

            window_size = transport.window

            header_length = transport.dataofs * 4

            payload_length = len(
                transport.payload
            )


        elif packet.haslayer(UDP):

            protocol = "UDP"

            transport = packet[UDP]

            src_port = transport.sport
            dst_port = transport.dport

            flags = None

            window_size = 0

            header_length = 8

            payload_length = len(
                transport.payload
            )


        else:

            # Ignore ICMP and other protocols
            return


        # -----------------------------------------------------
        # Packet length
        # -----------------------------------------------------

        packet_length = len(packet)


        # -----------------------------------------------------
        # Timestamp
        # -----------------------------------------------------

        timestamp = datetime.fromtimestamp(
            float(packet.time)
        )


        # -----------------------------------------------------
        # FLOW KEY
        # -----------------------------------------------------

        flow_key = self.get_flow_key(
            src_ip,
            src_port,
            dst_ip,
            dst_port,
            protocol
        )


        # -----------------------------------------------------
        # DETERMINE DIRECTION
        # -----------------------------------------------------

        if flow_key not in self.flow_directions:

            # First packet defines forward direction
            self.flow_directions[flow_key] = (
                src_ip,
                src_port
            )

            direction = "forward"

        else:

            original_src_ip, original_src_port = (
                self.flow_directions[flow_key]
            )

            if (
                src_ip == original_src_ip
                and
                src_port == original_src_port
            ):

                direction = "forward"

            else:

                direction = "backward"


        # -----------------------------------------------------
        # ADD PACKET TO FLOW TRACKER
        # -----------------------------------------------------

        self.flow_tracker.add_packet(

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


        # -----------------------------------------------------
        # DISPLAY PACKET INFORMATION
        # -----------------------------------------------------

        print(
            f"[PACKET] "
            f"{src_ip}:{src_port} -> "
            f"{dst_ip}:{dst_port} | "
            f"{protocol} | "
            f"{packet_length} bytes | "
            f"{direction}"
        )


    # =========================================================
    # START CAPTURE
    # =========================================================

    def start_capture(
        self,
        interface=None,
        packet_count=0
    ):

        self.running = True

        print()
        print("========================================")
        print("      AI-POWERED IDS")
        print("      PACKET CAPTURE STARTED")
        print("========================================")
        print()

        if interface:

            print(
                f"Interface: {interface}"
            )

        else:

            print(
                "Interface: Default"
            )

        print(
            "Press CTRL+C to stop capture."
        )

        print()


        try:

            sniff(

                iface=interface,

                prn=self.process_packet,

                count=packet_count,

                store=False
            )

        except KeyboardInterrupt:

            print()
            print(
                "Packet capture stopped by user."
            )

        except Exception as error:

            print()
            print(
                "Packet capture error:"
            )

            print(error)

        finally:

            self.running = False


    # =========================================================
    # STOP CAPTURE
    # =========================================================

    def stop_capture(self):

        self.running = False

        print(
            "Stopping packet capture..."
        )


    # =========================================================
    # GET ALL FLOWS
    # =========================================================

    def get_flows(self):

        return self.flow_tracker.get_all_flows()


    # =========================================================
    # GET FLOW COUNT
    # =========================================================

    def get_flow_count(self):

        return len(
            self.flow_tracker.get_all_flows()
        )


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    capture = PacketCapture()

    capture.start_capture(
        packet_count=20
    )

    print()
    print("========================================")
    print("CAPTURE SUMMARY")
    print("========================================")

    print(
        "Total Flows:",
        capture.get_flow_count()
    )