# ============================================================
# FitCom - Database Operations
# Author: Anand Kumar
# ============================================================

import streamlit as st
from database import SessionLocal
from models import Report, HIITSession


# ============================================================
# LOAD REPORTS
# ============================================================

def load_reports():
    """
    Load reports for the logged-in user only.
    """

    db = SessionLocal()

    try:
        user = st.session_state.get("user")

        if not user:
            return {}

        reports = db.query(Report).filter(
            Report.IsDeleted == False,
            Report.UserId == user
        ).all()

        result = {}

        for r in reports:
            data = r.__dict__.copy()

            # Remove SQLAlchemy internal key
            if "_sa_instance_state" in data:
                del data["_sa_instance_state"]

            # Group by Name
            if r.Name not in result:
                result[r.Name] = []

            result[r.Name].append(data)

        return result

    except Exception as e:
        print("Error loading reports:", e)
        return {}

    finally:
        db.close()


# ============================================================
# SAVE REPORT
# ============================================================

def save_report(name, data):
    """
    Save report into database.
    """

    db = SessionLocal()

    try:
        report = Report(**data)
        db.add(report)
        db.commit()

    except Exception as e:
        print("Error saving report:", e)

    finally:
        db.close()


# ============================================================
# LOAD HIIT SESSIONS
# ============================================================

def load_hiit_sessions(user):
    """
    Load HIIT sessions for logged-in user.
    """

    db = SessionLocal()

    try:
        if not user:
            return []

        sessions = db.query(HIITSession).filter(
            HIITSession.UserId == user,
            HIITSession.IsDeleted == False
        ).all()

        result = []

        for s in sessions:
            data = s.__dict__.copy()

            if "_sa_instance_state" in data:
                del data["_sa_instance_state"]

            result.append(data)

        return result

    except Exception as e:
        print("Error loading HIIT:", e)
        return []

    finally:
        db.close()