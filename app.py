from flask import Flask, request, g, jsonify
from db import SessionLocal
from services.event_service import create_event
from models import Alert
from detection.brute_force import detect_brute_force


app = Flask(__name__)

@app.before_request
def open_db_session():
    g.db = SessionLocal()


@app.teardown_request
def close_db_session(exception=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


@app.route("/events", methods=["POST"])
def ingest_event():
    data = request.get_json() or {}

    required_fields = ["timestamp", "ip", "event_type", "endpoint"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    event = create_event(g.db, data)

    return jsonify({
        "id": event.id,
        "message": "Event stored successfully"
    }), 201


@app.route("/alerts", methods=["GET"])
def list_alerts():
    alerts = (
        g.db.query(Alert)
        .order_by(Alert.created_at.desc())
        .all()
    )

    return jsonify([
        {
            "id": alert.id,
            "ip": alert.ip,
            "type": alert.alert_type,
            "count": alert.count,
            "window_seconds": alert.window_seconds,
            "created_at": alert.created_at.isoformat()
        }
        for alert in alerts
    ])

@app.route("/detect/bruteforce", methods=["POST"])
def run_bruteforce_detection():
    detect_brute_force(
        g.db,
        threshold=10,
        window_seconds=60
    )

    return jsonify({
        "message" : "Brute force detection executed"
    })


if __name__ == "__main__":
    app.run(debug=True)

