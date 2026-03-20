# -------------------------------------------------------
# FitCom - DB Storage Layer (FINAL PRODUCTION VERSION)
# Author: Anand Kumar
#
# Purpose:
# Central data access layer for:
# - Reports (Body Composition)
# - HIIT Sessions
# - User Authentication (Password)
#
# Design Principles:
# - Soft delete (no data loss)
# - DB-first (no CSV dependency)
# - Clean session handling
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
    NOTE: Using SHA256 (simple + sufficient for now)
    """
    return hashlib.sha256(password.encode()).hexdigest()


def set_user_password(name, password):
    """
    Set or update password for a user
    Applies to ALL records of that user
    """
    db = SessionLocal()
    try:
        hashed = hash_password(password)

        records = db.query(Report).filter(Report.Name == name).all()

        for r in records:
            r.Password = hashed  # store hashed password

        db.commit()

    finally:
        db.close()


def get_user_password(name):
    db = SessionLocal()
    try:
        record = db.query(Report)\
                   .filter(Report.Name == name)\
                   .first()

        # 🔥 SAFETY FIX (prevents crash if column missing)
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
    Save a new body composition report
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
    Load all ACTIVE reports (soft delete aware)
    Returns grouped dict:
    {
        "Anand": [ {...}, {...} ],
        "User2": [ {...} ]
    }
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

            # Remove SQLAlchemy internal key
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
    Soft delete a record based on user + index
    IMPORTANT: No actual deletion (data is preserved)
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
            record = records[index]

            # 🔥 Soft delete instead of hard delete
            record.IsDeleted = True

            db.commit()

    finally:
        db.close()


def update_record(name, date, updated_data):
    """
    Update latest record for a user on a specific date
    Handles duplicate-date edge case using latest ID
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
    Save a HIIT workout session into DB
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
    Load HIIT sessions
    - Can filter by user
    - Returns list of dicts
    """
    db = SessionLocal()
    try:
        query = db.query(HIITSession)\
                  .filter(HIITSession.IsDeleted == False)

        # Optional user filter
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
    Soft delete a HIIT session using ID
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