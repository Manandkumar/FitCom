# -------------------------------------------------------
# FitCom - DB Storage Layer (PRODUCTION SAFE)
# -------------------------------------------------------

from database import SessionLocal
from models import Report

# -------------------------------------------------------
# SAVE REPORT
# -------------------------------------------------------

def save_report(name, metrics):
    db = SessionLocal()
    try:
        report = Report(**metrics)
        db.add(report)
        db.commit()
    finally:
        db.close()


# -------------------------------------------------------
# LOAD REPORTS
# -------------------------------------------------------

def load_reports():
    db = SessionLocal()
    try:
        reports = db.query(Report).order_by(Report.Date).all()

        grouped = {}

        for r in reports:
            data = r.__dict__.copy()
            data.pop("_sa_instance_state", None)

            name = data["Name"]

            if name not in grouped:
                grouped[name] = []

            grouped[name].append(data)

        return grouped
    finally:
        db.close()


# -------------------------------------------------------
# DELETE RECORD (FIXED)
# -------------------------------------------------------

def delete_record(name, index):
    db = SessionLocal()
    try:
        records = db.query(Report)\
                    .filter(Report.Name == name)\
                    .order_by(Report.Date)\
                    .all()

        if 0 <= index < len(records):
            db.delete(records[index])
            db.commit()
    finally:
        db.close()


# -------------------------------------------------------
# UPDATE RECORD (SAFE)
# -------------------------------------------------------

def update_record(name, date, updated_data):
    db = SessionLocal()
    try:
        record = db.query(Report)\
                   .filter(Report.Name == name, Report.Date == date)\
                   .order_by(Report.id.desc())\
                   .first()

        if record:
            for key, value in updated_data.items():
                if hasattr(record, key):
                    setattr(record, key, value)

            db.commit()
    finally:
        db.close()