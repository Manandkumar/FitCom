# -------------------------------------------------------
# FitCom - DB Storage Layer (FINAL PRODUCTION VERSION)
# Author: Anand Kumar
# -------------------------------------------------------

from database import SessionLocal
from models import Report, HIITSession
import hashlib


# =======================================================
# 🔐 PASSWORD MANAGEMENT
# =======================================================

def hash_password(password):
    """
    Convert plain password into hashed version
    """
    return hashlib.sha256(password.encode()).hexdigest()


def set_user_password(name, password):
    """
    Set/update password for a user
    Updates ALL records for consistency
    """
    db = SessionLocal()
    try:
        hashed = hash_password(password)

        records = db.query(Report)\
                    .filter(Report.Name == name)\
                    .all()

        for r in records:
            r.Password = hashed

        db.commit()

    finally:
        db.close()


def get_user_password(name):
    """
    Get latest password for user (FIXED 🔥)
    Ensures correct password when multiple records exist
    """
    db = SessionLocal()
    try:
        record = db.query(Report)\
                   .filter(Report.Name == name)\
                   .order_by(Report.id.desc())\  # 🔥 CRITICAL FIX
                   .first()

        if not record:
            return None

        return getattr(record, "Password", None)

    finally:
        db.close()


# =======================================================
# 📊 REPORTS (BODY COMPOSITION)
# =======================================================

def save_report(name, metrics):
    """
    Save new report
    """
    db = SessionLocal()
    try:
        report = Report(**metrics)
        db.add(report)
        db.commit()

    finally:
        db.close()


def load_reports():
    """
    Load ACTIVE reports only
    """
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


def delete_record(name, index):
    """
    Soft delete report
    """
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
            records[index].IsDeleted = True
            db.commit()

    finally:
        db.close()


def update_record(name, date, updated_data):
    """
    Update latest record for given date
    """
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
# 🔥 HIIT WORKOUT STORAGE
# =======================================================

def save_hiit_session(data):
    """
    Save HIIT session
    """
    db = SessionLocal()
    try:
        session = HIITSession(**data)
        db.add(session)
        db.commit()

    finally:
        db.close()


def load_hiit_sessions(name=None):
    """
    Load HIIT sessions (optional user filter)
    """
    db = SessionLocal()
    try:
        query = db.query(HIITSession)\
                  .filter(HIITSession.IsDeleted == False)

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


def delete_hiit_session(session_id):
    """
    Soft delete HIIT session
    """
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