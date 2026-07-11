# Great Filter

![Status](https://img.shields.io/badge/status-experimental-yellow)

A lightweight, real-time network defense tool for Windows that detects and blocks IP addresses flooding a machine with packets, using a simple packet-rate threshold and the Windows Firewall. Includes a companion traffic simulator so you can test the blocker safely against your own machine.

> ⚠️ **Use responsibly.** The included attack simulator generates real network traffic. Only run it against hosts and networks you own or have explicit permission to test. Using it against systems you don't control may violate the law and third-party terms of service.

## Features

- **Real-time packet sniffing** using Scapy to monitor all inbound IP traffic.
- **Sliding-window rate detection** — tracks packets per source IP over a rolling 1-second window.
- **Automatic mitigation** — adds a Windows Firewall rule to block any IP that exceeds the configured threshold.
- **Attack simulator included** — a companion script to safely generate test traffic and validate the blocker works.
- **Zero external service dependencies** — everything runs locally with Python and the native Windows Firewall.

## How It Works

`dos_blocker_enhanced.py` sniffs live IP traffic and keeps a per-source-IP timestamp log. For every packet received, it recalculates how many packets that source IP has sent in the last second. If that rate crosses the `THRESHOLD` (40 packets/sec by default), the script:

1. Prints a warning with the offending IP and its current rate.
2. Adds a blocking rule to Windows Firewall via `netsh advfirewall`.
3. Adds the IP to an in-memory blocklist so it's ignored on subsequent packets.

`dos_blocker_tester_enhanced.py` is a standalone traffic generator. It sends a configurable number of TCP packets to a target IP over a configurable duration, letting you simulate a flood and confirm the blocker reacts correctly.

## Prerequisites

- **Windows OS** (the blocker uses `netsh advfirewall`, a Windows-only command).
- **Python 3.7+**
- **[Npcap](https://npcap.com/#download)** — required for Scapy to capture packets on Windows. Install with "WinPcap API-compatible mode" enabled.
- **Administrator privileges** — both packet sniffing and firewall rule creation require running as Administrator.
- **[Scapy](https://scapy.net/)** Python package.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/kernel-pwn/great_filter.git
   cd great_filter
   ```

2. Install the Python dependency:

   ```bash
   pip install scapy
   ```

3. Install [Npcap](https://npcap.com/#download) if it isn't already on your system (required by Scapy for live packet capture on Windows).

> There is currently no `requirements.txt` in the repository. Consider running `pip freeze > requirements.txt` after installing dependencies and committing it for reproducible installs.

## Usage

### Running the Blocker

Open a terminal **as Administrator** (or run your IDE, e.g. PyCharm, as Administrator) and run:

```bash
python dos_blocker_enhanced.py
```

Expected output:

```
THRESHOLD: 40 packets/sec
Monitoring network traffic on Windows... Press Ctrl+C to stop.
```

The script will now watch all incoming IP traffic. If a source IP exceeds the packet-rate threshold, you'll see:

```
Blocking IP: 203.0.113.42 | Current Rate: 57 pkts/sec
```

...and a matching rule (named `Block_DDoS_<ip>`) will appear in Windows Defender Firewall > Advanced Settings > Inbound Rules.

Press `Ctrl+C` at any time to stop monitoring.

### Running the Attack Simulator

In a **second terminal**, run the tester to generate test traffic against a target (defaults to `127.0.0.1`):

```bash
python dos_blocker_tester_enhanced.py
```

Expected output:

```
Starting attack simulation against 127.0.0.1...
Sending 100 packets over 2 seconds (Target rate: 50.0 pkts/sec)
Simulation finished. Sent 100 packets in 2.01 seconds.
```

Since the default rate (50 pkts/sec) exceeds the blocker's threshold (40 pkts/sec), the blocker terminal should detect and block the simulated source shortly after the run starts.

## Configuration

Both scripts use plain constants at the top of the file — edit them directly to change behavior:

**`dos_blocker_enhanced.py`**

| Constant    | Default | Description                                      |
|-------------|---------|---------------------------------------------------|
| `THRESHOLD` | `40`    | Max packets/sec from a single source IP before it's blocked. |

**`dos_blocker_tester_enhanced.py`**

| Constant       | Default       | Description                                  |
|----------------|---------------|-----------------------------------------------|
| `TARGET_IP`    | `"127.0.0.1"` | IP address to send test traffic to.           |
| `NUM_PACKETS`  | `100`         | Total number of packets to send.              |
| `DURATION`     | `2`           | Time (seconds) to spread the packets over.     |

To unblock an IP after testing, remove the corresponding rule from Windows Defender Firewall (Advanced Settings > Inbound Rules > `Block_DDoS_<ip>`), or run:

```bash
netsh advfirewall firewall delete rule name="Block_DDoS_<ip>"
```

## Project Structure

```
great_filter/
├── dos_blocker_enhanced.py          # Real-time sniffer + firewall-based IP blocker
├── dos_blocker_tester_enhanced.py   # Traffic generator for testing the blocker
└── README.md
```

## Contributing

Contributions are welcome. To contribute:

1. **Fork** the repository.
2. **Create a branch** for your change:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**, following the existing code style. Please:
   - Keep functions focused and add docstrings for anything non-trivial.
   - Avoid adding external dependencies unless necessary; if you do, update the installation instructions.
   - Test that the blocker and simulator still run correctly together (see [Usage](#usage)).
4. **Commit your changes** with a clear, descriptive message:

   ```bash
   git commit -m "Add: brief description of the change"
   ```

5. **Push to your fork** and **open a Pull Request** against `main`, describing:
   - What the change does and why.
   - How you tested it.
   - Any breaking changes or new dependencies.

For larger changes (new features, architecture changes), please open an issue first to discuss the approach before submitting a PR.

### Reporting Issues

If you find a bug or have a feature request, open a GitHub issue with:
- Your OS and Python version.
- Steps to reproduce (for bugs).
- Expected vs. actual behavior.
