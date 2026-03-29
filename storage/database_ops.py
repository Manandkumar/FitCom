# ============================================================
# FitCom - Database Operations
# Author: Anand Kumar
# ============================================================

import streamlit as st
import sys
import os

# ------------------------------------------------------------
# FIX: Ensure project root is accessible (IMPORTANT)
# ------------------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Now safe to import
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
            data.pop("_sa_instance_state", None)

            # Group reports by Name
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

            # Remove SQLAlchemy internal key
            data.pop("_sa_instance_state", None)

            result.append(data)

        return result

    except Exception as e:
        print("Error loading HIIT:", e)
        return []

    finally:
        db.close()