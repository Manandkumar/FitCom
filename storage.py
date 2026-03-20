# -------------------------------------------------------
# FitCom - DB Storage Layer (FINAL VERSION 🔥)
# Author: Anand Kumar
# -------------------------------------------------------

from database import SessionLocal
from models import Report, HIITSession
import hashlib


# =======================================================
# 🔐 PASSWORD MANAGEMENT (OPTIONAL / LEGACY)
# =======================================================

def hash_password(password):
    """Convert plain password into SHA256 hash"""
    return hashlib.sha256(password.encode()).hexdigest()


def set_user_password(name, password):
    """
    Update password for all records of a user
    (Not used in current simplified login)
    """
    db = SessionLocal()
    try:
        hashed = hash_password(password)

        # Direct SQL update (efficient)
        db.query(Report).filter(Report.Name == name).update(
            {"Password": hashed},
            synchronize_session=False
        )

        db.commit()

    except Exception as e:
        print("❌ Password update error:", e)
        db.rollback()

    finally:
        db.close()


def get_user_password(name):
    """
    Fetch latest non-null password
    (Used only if password-based auth is enabled)
    """
    db = SessionLocal()
    try:
        record = (
            db.query(Report.Password)
            .filter(Report.Name == name)
            .filter(Report.Password != None)
            .order_by(Report.id.desc())
            .first()
        )

        return record[0] if record else None

    finally:
        db.close()


# =======================================================
# 📊 REPORTS (BODY COMPOSITION DATA)
# =======================================================

def save_report(name, metrics):
    """
    Save new body composition record
    Preserves password from last record (if exists)
    """
    db = SessionLocal()
    try:
        # Get latest record for password preservation
        existing = (
            db.query(Report)
            .filter(Report.Name == name)
            .order_by(Report.id.desc())
            .first()
        )

        if existing and getattr(existing, "Password", None):
            metrics["Password"] = existing.Password

        db.add(Report(**metrics))
        db.commit()

    except Exception as e:
        print("❌ Save report error:", e)
        db.rollback()

    finally:
        db.close()


def load_reports():
    """
    Load all active reports and group by user
    """
    db = SessionLocal()
    try:
        reports = db.query(Report).filter(Report.IsDeleted == False).all()

        grouped = {}

        for r in reports:
            data = r.__dict__.copy()
            data.pop("_sa_instance_state", None)

            name = data["Name"]
            grouped.setdefault(name, []).append(data)

        return grouped

    finally:
        db.close()


def delete_record(name, index):
    """
    Soft delete a report record (keeps DB history)
    """
    db = SessionLocal()
    try:
        records = db.query(Report).filter(
            Report.Name == name,
            Report.IsDeleted == False
        ).all()

        if 0 <= index < len(records):
            records[index].IsDeleted = True
            db.commit()

    except Exception as e:
        print("❌ Delete error:", e)

    finally:
        db.close()


def update_record(name, date, updated_data):
    """
    Update latest record for a given date
    """
    db = SessionLocal()
    try:
        record = (
            db.query(Report)
            .filter(
                Report.Name == name,
                Report.Date == date,
                Report.IsDeleted == False
            )
            .order_by(Report.id.desc())
            .first()
        )

        if record:
            for key, value in updated_data.items():
                if hasattr(record, key):
                    setattr(record, key, value)

            db.commit()

    except Exception as e:
        print("❌ Update error:", e)
        db.rollback()

    finally:
        db.close()


# =======================================================
# 🔥 HIIT WORKOUT STORAGE (FULL VERSION 🔥🔥🔥)
# =======================================================

def save_hiit_session(data):
    """
    Save HIIT session safely

    Supports:
    - Calories 🔥
    - Heart Rate ❤️
    - Duration ⏱️
    - Notes 📝

    Works even if DB schema is partially missing fields
    """
    db = SessionLocal()
    try:
        session = HIITSession(
            Name=data.get("Name"),
            Date=data.get("Date"),
            Workout=data.get("Workout"),
            Calories=data.get("Calories"),

            # Optional fields (safe defaults)
            HeartRate=data.get("HeartRate", None),
            Duration=data.get("Duration", None),
            Notes=data.get("Notes", None),

            IsDeleted=False
        )

        db.add(session)
        db.commit()

    except Exception as e:
        print("❌ HIIT SAVE ERROR:", e)
        db.rollback()

    finally:
        db.close()


def load_hiit_sessions(name=None):
    """
    Load HIIT sessions safely

    Only selects known columns → avoids Supabase crash
    """
    db = SessionLocal()
    try:
        # Select only required columns (avoids schema mismatch crash)
        query = db.query(
            HIITSession.id,
            HIITSession.Name,
            HIITSession.Date,
            HIITSession.Workout,
            HIITSession.Calories,
            HIITSession.HeartRate,
            HIITSession.Duration,
            HIITSession.Notes
        ).filter(HIITSession.IsDeleted == False)

        # Optional user filter
        if name:
            query = query.filter(HIITSession.Name == name)

        rows = query.all()

        # Convert to dictionary list (UI-friendly)
        result = []
        for r in rows:
            result.append({
                "id": r.id,
                "Name": r.Name,
                "Date": r.Date,
                "Workout": r.Workout,
                "Calories": r.Calories,
                "HeartRate": r.HeartRate,
                "Duration": r.Duration,
                "Notes": r.Notes
            })

        return result

    except Exception as e:
        print("❌ HIIT LOAD ERROR:", e)
        return []

    finally:
        db.close()


def delete_hiit_session(session_id):
    """
    Soft delete HIIT session
    """
    db = SessionLocal()
    try:
        record = db.query(HIITSession).filter(
            HIITSession.id == session_id
        ).first()

        if record:
            record.IsDeleted = True
            db.commit()

    except Exception as e:
        print("❌ HIIT delete error:", e)

    finally:
        db.close()