# SEPS — Security Event Processing System

Experimental security system inspired by SIEM/WAF architectures.

## Current features
- Event ingestion API
- SQLAlchemy data models
- Alert creation with IP reputation tracking
- Basic detection pipeline (WIP)

## Goal
Hands-on study project focused on security engineering and system design.

```bash
git clone <repo>
cd seps
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python create_db.py
python app.py
