import requests
import time
from datetime import datetime, timezone

URL = "http://127.0.0.1:5000/events"

IP = "10.0.0.61"
TOTAL_EVENTS = 20

for i in range(TOTAL_EVENTS):
    event = {
        "timestamp":datetime.utcnow().isoformat(),
        "ip":IP,
        "event_type":"login_failed",
        "endpoint":"/login"}
    response = requests.post(URL, json=event)
    print(f"Sent event {i+1} -> status {response.status_code}")
    time.sleep(0.2)

