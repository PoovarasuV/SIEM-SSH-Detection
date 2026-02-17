import subprocess
import json
import re
from datetime import datetime

failed_attempts = {}
alerted_ips = set()
alert_file = open("alerts.log", "a")

process = subprocess.Popen(
    ["journalctl", "-u", "ssh", "-f", "-o", "json"],
    stdout=subprocess.PIPE,
    text=True
)

print("🔍 Live SSH monitoring started...\n")

for line in process.stdout:
    if line.strip() == "":
        continue

    try:
        log_data = json.loads(line)
    except json.JSONDecodeError:
        continue

    message = log_data.get("MESSAGE", "")

    # Extract timestamp
    timestamp_micro = log_data.get("__REALTIME_TIMESTAMP")

    if timestamp_micro:
        timestamp = datetime.fromtimestamp(int(timestamp_micro) / 1_000_000)
        readable_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    else:
        readable_time = "UNKNOWN_TIME"

    # Detect attack types
    if "Failed password" in message or "Invalid user" in message:

        if "Failed password" in message:
            match = re.search(r"Failed password for (\w+) from ([\d\.:]+)", message)

        elif "Invalid user" in message:
            match = re.search(r"Invalid user (\w+) from ([\d\.:]+)", message)

        else:
            match = None

        if match:
            username = match.group(1)
            ip_address = match.group(2)

            failed_attempts[ip_address] = failed_attempts.get(ip_address, 0) + 1

            if failed_attempts[ip_address] >= 3 and ip_address not in alerted_ips:
                alerted_ips.add(ip_address)

                print("🚨 BRUTE FORCE ALERT")
                print("Time:", readable_time)
                print("Username:", username)
                print("Source IP:", ip_address)
                print("Failed Attempts:", failed_attempts[ip_address])
                print("------------------------")

                alert_message = f"{readable_time} | BRUTE FORCE ALERT | User: {username} | IP: {ip_address} | Attempts: {failed_attempts[ip_address]}\n"
                alert_file.write(alert_message)
                alert_file.flush()
