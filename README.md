Enterprise Log Threat Detection System | Python-Based SIEM
Project Overview

This project is a real-time SSH log monitoring and threat detection system built using Python. It simulates core SIEM (Security Information and Event Management) capabilities by analyzing live system logs, detecting suspicious authentication behavior, and generating structured security alerts.

The system focuses on identifying brute-force login attempts and invalid user enumeration attacks using threshold-based anomaly detection techniques.

This project demonstrates practical Blue Team skills including log analysis, event correlation, alert engineering, and SOC-style monitoring.

Key Objectives

Monitor SSH authentication logs in real time

Detect repeated failed login attempts from the same IP

Identify invalid username enumeration attempts

Generate structured, timestamped security alerts

Simulate real-world SOC monitoring workflows

Features
Real-Time Log Monitoring

Uses journalctl to stream SSH logs live

Parses logs in structured JSON format

Brute-Force Attack Detection

Detects:

Failed password events

Invalid user login attempts

Triggers alert when:

3 or more failed attempts occur from the same IP address

Threshold-Based Correlation Logic

Maintains IP-based attempt tracking

Prevents duplicate alert flooding

Simulates basic SIEM correlation rule behavior

Structured Alert Generation

Each alert includes:

Timestamp

Username

Source IP address

Failed attempt count

Persistent Logging

Alerts are written to alerts.log

Supports forensic review and evidence preservation

Technologies Used

Python 3

Regular Expressions (Regex)

JSON log parsing

Linux journalctl

Linux system authentication logs

Detection Logic Workflow

Continuously monitors SSH logs using:

journalctl -u ssh -f -o json


Parses each log entry as JSON.

Extracts:

MESSAGE

__REALTIME_TIMESTAMP

Applies regex patterns to detect:

Failed password attempts

Invalid user attempts

Tracks failed attempts per IP address.

Triggers alert if attempts ≥ 3.

Writes structured alert to terminal and alerts.log.

Example Alert Output
BRUTE FORCE ALERT
Time: 2026-02-16 22:17:07
Username: testuser
Source IP: ::1
Failed Attempts: 3


Saved in alerts.log as:

2026-02-16 22:17:07 | BRUTE FORCE ALERT | User: testuser | IP: ::1 | Attempts: 3

