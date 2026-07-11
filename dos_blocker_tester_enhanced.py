import sys
import time
from scapy.all import send
from scapy.layers.inet import IP, TCP

# 1. Update this to your local target (e.g., your loopback '127.0.0.1' or your router/local VM)
TARGET_IP = "127.0.0.1"
NUM_PACKETS = 100
DURATION = 2  # Total time to stretch the packets over


def send_packets(target_ip, num_packets, duration):
    # Layer 3 packet - Scapy handles the Ethernet layer automatically with send()
    packet = IP(dst=target_ip) / TCP()

    print(f"Starting attack simulation against {target_ip}...")
    print(
        f"Sending {num_packets} packets over {duration} seconds (Target rate: {num_packets / duration:.1f} pkts/sec)")

    start_time = time.time()
    end_time = start_time + duration
    packet_count = 0

    # Calculate exact delay needed between packets to match the duration
    delay = duration / num_packets

    while time.time() < end_time and packet_count < num_packets:
        # send() automatically handles routing on Windows
        send(packet, verbose=False)
        packet_count += 1

        # Pacing out the packets so it doesn't dump all 100 in the first millisecond
        time.sleep(delay)

    total_time = time.time() - start_time
    print(f"Simulation finished. Sent {packet_count} packets in {total_time:.2f} seconds.")


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        print("This script requires Python 3.")
        sys.exit(1)

    send_packets(TARGET_IP, NUM_PACKETS, DURATION)