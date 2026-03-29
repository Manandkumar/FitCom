from database import SessionLocal
from models import Report, HIITSession
import hashlib


# =======================================================
# 🔐 PASSWORD MANAGEMENT
# =======================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def set_user_password(name, password):
    db = SessionLocal()
    try:
        hashed = hash_password(password)

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
    db = SessionLocal()
    try:
        record = (
            db.query(Report.Password)
            .filter(Report.Name == name)
            .filter(Report.Password.isnot(None))
            .order_by(Report.id.desc())
            .first()
        )

        return record[0] if record else None

    except Exception as e:
        print("❌ Password fetch error:", e)
        return None
    finally:
        db.close()


# =======================================================
# 📊 REPORTS
# =======================================================

def save_report(name, metrics):
    db = SessionLocal()
    try:
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
    db = SessionLocal()
    try:
        reports = db.query(Report).filter(Report.IsDeleted == False).all()

        grouped = {}

        for r in reports:
            data = {k: v for k, v in r.__dict__.items() if k != "_sa_instance_state"}
            name = data.get("Name", "Unknown")

            grouped.setdefault(name, []).append(data)

        return grouped

    except Exception as e:
        print("❌ Load reports error:", e)
        return {}
    finally:
        db.close()


def delete_record(name, index):
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
        db.rollback()
    finally:
        db.close()


def update_record(name, date, updated_data):
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
# 🔥 HIIT SESSIONS
# =======================================================

def save_hiit_session(data):
    db = SessionLocal()
    try:
        session = HIITSession(
            Name=data.get("Name"),
            Date=data.get("Date"),
            Workout=data.get("Workout"),
            Calories=data.get("Calories"),
            HeartRate=data.get("HeartRate"),
            Duration=data.get("Duration"),
            Notes=data.get("Notes"),
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
    db = SessionLocal()
    try:
        query = db.query(HIITSession).filter(HIITSession.IsDeleted == False)

        if name:
            query = query.filter(HIITSession.Name == name)

        rows = query.all()

        return [
            {k: v for k, v in r.__dict__.items() if k != "_sa_instance_state"}
            for r in rows
        ]

    except Exception as e:
        print("❌ HIIT LOAD ERROR:", e)
        return []
    finally:
        db.close()


def delete_hiit_session(session_id):
    db = SessionLocal()
    try:
        record = db.query(HIITSession).filter(HIITSession.id == session_id).first()

        if record:
            record.IsDeleted = True
            db.commit()

    except Exception as e:
        print("❌ HIIT delete error:", e)
        db.rollback()
    finally:
        db.close()