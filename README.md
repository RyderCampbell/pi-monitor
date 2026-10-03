# pi-monitor

Small Python scripts for monitoring a Raspberry Pi (or any Linux box) from the command line.

## Scripts

| Script | What it shows | Needs |
|---|---|---|
| `bandwidth.py` | Live RX/TX throughput in Mbit/s for a network interface | Linux (`ip` command) |
| `pi_temp.py` | CPU temperature in °C and °F every 5 seconds | Raspberry Pi (`vcgencmd`) |

No extra packages needed, just Python 3.

## Usage

```bash
python3 bandwidth.py          # defaults to eth0
python3 bandwidth.py wlan0    # pick another interface
python3 pi_temp.py
```

Press `Ctrl+C` to stop.

## How it works

Each script runs a built-in Linux command, parses its text output, and prints a clean reading.
Bandwidth is calculated from the change in byte counters over one second.

## Next up

- Combine the scripts into a single web dashboard with live charts
- Add latency and packet-loss monitoring with configurable targets
