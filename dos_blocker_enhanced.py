import os
import sys
import time
import ctypes
from collections import defaultdict
from scapy.all import sniff
from scapy.layers.inet import IP

THRESHOLD = 40
print(f"THRESHOLD: {THRESHOLD} packets/sec")

packet_timestamps = defaultdict(list)
blocked_ips = set()


def packet_callback(packet):
    if not packet.haslayer(IP):
        return

    src_ip = packet[IP].src
    if src_ip in blocked_ips:
        return

    current_time = time.time()
    packet_timestamps[src_ip].append(current_time)
    packet_timestamps[src_ip] = [t for t in packet_timestamps[src_ip] if current_time - t <= 1.0]

    packet_rate = len(packet_timestamps[src_ip])

    if packet_rate > THRESHOLD:
        print(f"Blocking IP: {src_ip} | Current Rate: {packet_rate} pkts/sec")

        # Windows Firewall Command to block an IP
        rule_name = f"Block_DDoS_{src_ip}"
        os.system(f'Netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block remoteip={src_ip}')

        blocked_ips.add(src_ip)
        del packet_timestamps[src_ip]


if __name__ == "__main__":
    # Windows equivalent of checking for root (Checking for Administrator privileges)
    try:
        is_admin = os.getuid() == 0  # Just a fallback, but on Windows we use ctypes:
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    if not is_admin:
        print("Error: This script requires Administrator privileges.")
        print("Please restart PyCharm as Administrator, or run your command prompt as Admin.")
        sys.exit(1)

    print("Monitoring network traffic on Windows... Press Ctrl+C to stop.")
    try:
        sniff(filter="ip", prn=packet_callback, store=0)
    except KeyboardInterrupt:
        print("\nStopping monitor.")