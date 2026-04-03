# SEPS — Security Event Processing System

SEPS is a lightweight security event processing system inspired by SIEM (Security Information and Event Management) tools.

It ingests events, detects suspicious behavior (such as brute force attacks), generates alerts, and maintains IP reputation - all in near real-time.

---

## Features

- Event ingestion via REST API
- Brute force attack detection
- Alert generation with severity levels
- IP reputation tracking
- System atatistics endpoint
- Near real-time detection (triggered on event ingestion)
- Alert deduplication

---

## Architecture Overview

Events -> API -> Database -> Detection Engine -> Alerts -> Reputation

### Flow:

1. Events are sent to `/events`
2. Stored in database
3. Detection runs automatically
4. Alerts are generated if thresholds are met
5. IP reputation is updated
6. Data can be queried via API

---

## API Endpoints

### Ingest Event

POST /events
**Body:**

```json
{
    "timestamp": "2026-03-13T21:00:00",
    "ip": "10.0.0.66",
    "event_type": "login_failed",
    "endpoint": "/login"
}
```
### Get Alerts

GET /alerts

### Run Detection (manual - optional)

POST /detect/bruteforce

### Get IP Reputation

GET /reputation/<ip>

### System Stats

GET /stats

```json
{
    "events_total": 20,
    "alerts_total": 1,
    "ips_flagged": 1
}
```
---
## Detection Logic

Brute force detection is based on:
  - event_type = login_failded
  - Time window (e.g., 60 seconds)
  - Threshold (e.g., 10 attempts)

If exceeded:
  - Alert is generated
  - Severity assigned (e.g., high)
  - IP reputation increases
---

## Reputation System

Reputation score increases based on alert severity:

Severity                        Risk Increment
---
low                             +5
---
medium                          +10
---
high                            +20
---
critical                        +40
---

---

## Setup

```bash
git clone https://github.com/mateusKing123/seps-security-event-processing-system.git
cd seps

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python create_db.py
python app.py
```

---

## Generate Test Data
Use the provided script:

```bash
python generate_logs.py
```
This simulates a brute force attack.

---

## Tech Stack
  - Python
  - Flask
  - SQLAlchemy
  - SQLite

---

## Future Improvements
  - Asynchronous processing (queue/workers)
  - Multiple detection rules
  - Alert history tracking
  - Dashboard / UI
  - PostgreSQL supports
  - detection/anomaly
  - detection/api_abuse
  - simulator/attack_simulatior

---

## Purpose

This project was built to demonstrate:
  - Backend system design
  - Event-driven architecture
  - Security detection concepts
  - Data processing pipelines

---

## Author

Mateus Camargo
