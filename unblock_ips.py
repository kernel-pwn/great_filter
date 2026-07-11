import os
import ctypes
import sys

# Add any IPs you want to unblock to this list
IPS_TO_UNBLOCK = ["127.0.0.1"]


def unblock_ips():
    # Admin check
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        is_admin = os.getuid() == 0

    if not is_admin:
        print("Error: This script requires Administrator privileges.")
        sys.exit(1)

    for ip in IPS_TO_UNBLOCK:
        rule_name = f"Block_DDoS_{ip}"
        print(f"Removing firewall rule for: {ip}")
        # Execute the delete command
        os.system(f'netsh advfirewall firewall delete rule name="{rule_name}"')

    print("Cleanup complete.")


if __name__ == "__main__":
    unblock_ips()