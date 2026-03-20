# -------------------------------------------------------
# FitCom - DB Storage Layer (FINAL PRODUCTION VERSION)
# -------------------------------------------------------

from database import SessionLocal
from models import Report, HIITSession


# =======================================================
# SAVE REPORT
# =======================================================

def save_report(name, metrics):
    db = SessionLocal()
    try:
        report = Report(**metrics)
        db.add(report)
        db.commit()
    finally:
        db.close()


# =======================================================
# LOAD REPORTS (ONLY ACTIVE)
# =======================================================

def load_reports():
    db = SessionLocal()
    try:
        reports = db.query(Report)\
                    .filter(Report.IsDeleted == False)\
                    .order_by(Report.Date)\
                    .all()

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


# =======================================================
# DELETE REPORT (SOFT DELETE)
# =======================================================

def delete_record(name, index):
    db = SessionLocal()
    try:
        records = db.query(Report)\
                    .filter(
                        Report.Name == name,
                        Report.IsDeleted == False
                    )\
                    .order_by(Report.Date)\
                    .all()

        if 0 <= index < len(records):
            record = records[index]

            # 🔥 Soft delete
            record.IsDeleted = True

            db.commit()

    finally:
        db.close()


# =======================================================
# UPDATE REPORT
# =======================================================

def update_record(name, date, updated_data):
    db = SessionLocal()
    try:
        record = db.query(Report)\
                   .filter(
                       Report.Name == name,
                       Report.Date == date,
                       Report.IsDeleted == False
                   )\
                   .order_by(Report.id.desc())\
                   .first()

        if record:
            for key, value in updated_data.items():
                if hasattr(record, key):
                    setattr(record, key, value)

            db.commit()

    finally:
        db.close()


# =======================================================
# HIIT - SAVE SESSION
# =======================================================

def save_hiit_session(data):
    db = SessionLocal()
    try:
        session = HIITSession(**data)
        db.add(session)
        db.commit()
    finally:
        db.close()


# =======================================================
# HIIT - LOAD SESSIONS (ONLY ACTIVE)
# =======================================================

def load_hiit_sessions(name=None):
    db = SessionLocal()
    try:
        query = db.query(HIITSession)\
                  .filter(HIITSession.IsDeleted == False)

        # Optional filter by user
        if name:
            query = query.filter(HIITSession.Name == name)

        sessions = query.order_by(HIITSession.Date).all()

        result = []

        for s in sessions:
            data = s.__dict__.copy()
            data.pop("_sa_instance_state", None)
            result.append(data)

        return result

    finally:
        db.close()


# =======================================================
# HIIT - DELETE SESSION (SOFT DELETE)
# =======================================================

def delete_hiit_session(session_id):
    db = SessionLocal()
    try:
        record = db.query(HIITSession)\
                   .filter(HIITSession.id == session_id)\
                   .first()

        if record:
            record.IsDeleted = True
            db.commit()

    finally:
        db.close()