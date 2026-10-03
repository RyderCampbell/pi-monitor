import subprocess
import sys
import time

INTERVAL = 5  # seconds between readings


def get_pi_temp():
    try:
        results = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True)
    except FileNotFoundError:
        sys.exit("Error: 'vcgencmd' was not found. This script needs a Raspberry Pi.")
    return results.stdout


def clean_pi_temp(raw_temp):
    for line in raw_temp.split("\n"):
        if "temp" in line:
            return float(line.split("=")[1].split("'")[0])
    return None


def get_fahrenheit(celsius_temp):
    return (celsius_temp * 1.8) + 32


if __name__ == "__main__":
    print("Monitoring Raspberry Pi temperature (Ctrl+C to stop)")
    try:
        while True:
            celsius_temp = clean_pi_temp(get_pi_temp())
            if celsius_temp is None:
                print("Could not read temperature, retrying...")
            else:
                fahrenheit_temp = get_fahrenheit(celsius_temp)
                print(f"Pi temperature: {celsius_temp:.1f} °C / {fahrenheit_temp:.1f} °F")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nStopped.")
