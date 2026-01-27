from db import SessionLocal
from detection.brute_force import detect_brute_force
from services.alert_service import create_alert_from_detection

def run_detection():
    db = SessionLocal()

    try:
        detections = detect_brute_force(
            db,
            max_attempts=5,
            window_seconds=300
        )

        for d in detections:
            create_alert_from_detection(
                db,
                alert_type="brute_force",
                ip=d["ip"],
                count=d["attemps"],
                window_seconds=d["window_seconds"]
            )

    finally:
        db.close()

if __name__=="__main__":
    run_detection()