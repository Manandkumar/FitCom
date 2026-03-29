# ============================================================
# FitCom - Database Operations
# Author: Anand Kumar
# ============================================================

import streamlit as st

# ------------------------------------------------------------
# PROPER PACKAGE IMPORTS (NO HACKS)
# ------------------------------------------------------------

from ..database import SessionLocal
from ..models import Report, HIITSession


# ============================================================
# LOAD REPORTS
# ============================================================

def load_reports():
    """
    Load reports for the logged-in user only.
    Groups data by Name.
    """

    db = SessionLocal()

    try:
        user = st.session_state.get("user")

        if not user:
            return {}

        # Fetch only user-specific active reports
        reports = db.query(Report).filter(
            Report.IsDeleted == False,
            Report.UserId == user
        ).all()

        result = {}

        for r in reports:
            data = r.__dict__.copy()

            # Remove SQLAlchemy internal metadata
            data.pop("_sa_instance_state", None)

            # Group reports by Name
            result.setdefault(r.Name, []).append(data)

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
    Save a new report into the database.
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
    Load HIIT sessions for the logged-in user.
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

            # Remove SQLAlchemy internal metadata
            data.pop("_sa_instance_state", None)

            result.append(data)

        return result

    except Exception as e:
        print("Error loading HIIT sessions:", e)
        return []

    finally:
        db.close()