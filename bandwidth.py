import subprocess
import sys
import time

INTERFACE = sys.argv[1] if len(sys.argv) > 1 else "eth0"
INTERVAL = 1  # seconds between readings


def get_interface_stats(interface):
    try:
        results = subprocess.run(["ip", "-s", "link", "show", interface], capture_output=True, text=True)
    except FileNotFoundError:
        sys.exit("Error: the 'ip' command was not found. This script needs Linux.")
    if results.returncode != 0:
        sys.exit(f"Error: could not read interface '{interface}'. Check the name with 'ip link'.")
    return results.stdout


def clean_interface_stats(raw_stats):
    rx_bytes = tx_bytes = None
    lines = raw_stats.split("\n")
    for index, line in enumerate(lines):
        if "RX:" in line:
            rx_bytes = int(lines[index + 1].split()[0])
        if "TX:" in line:
            tx_bytes = int(lines[index + 1].split()[0])
    return rx_bytes, tx_bytes


def bytes_to_mbits(bytes_after, bytes_before, time_elapsed):
    return (bytes_after - bytes_before) * 8 / time_elapsed / 1_000_000


if __name__ == "__main__":
    print(f"Monitoring {INTERFACE} (Ctrl+C to stop)")
    try:
        while True:
            rx_before, tx_before = clean_interface_stats(get_interface_stats(INTERFACE))
            time.sleep(INTERVAL)
            rx_after, tx_after = clean_interface_stats(get_interface_stats(INTERFACE))

            if None in (rx_before, tx_before, rx_after, tx_after):
                print("Could not parse interface stats, retrying...")
                continue

            rx_mbits = bytes_to_mbits(rx_after, rx_before, INTERVAL)
            tx_mbits = bytes_to_mbits(tx_after, tx_before, INTERVAL)
            print(f"RX: {rx_mbits:.2f} Mbit/s | TX: {tx_mbits:.2f} Mbit/s")
    except KeyboardInterrupt:
        print("\nStopped.")
