# ============================================================
# FitCom - Storage Layer
# Author: Anand Kumar
# ============================================================

import streamlit as st
from database import SessionLocal
from models import Report, HIITSession


# ============================================================
# LOAD REPORTS (USER FILTERED)
# ============================================================

def load_reports():
    """
    Load reports only for the logged-in user.
    """

    db = SessionLocal()

    try:
        user = st.session_state.get("user")

        # If no user logged in, return empty
        if not user:
            return {}

        reports = db.query(Report).filter(
            Report.IsDeleted == False,
            Report.UserId == user
        ).all()

        result = {}

        for r in reports:
            data = r.__dict__.copy()

            # Remove SQLAlchemy internal field
            data.pop("_sa_instance_state", None)

            # Group by Name
            result.setdefault(r.Name, []).append(data)

        return result

    finally:
        db.close()


# ============================================================
# SAVE REPORT
# ============================================================

def save_report(name, data):
    """
    Save a new report to database.
    """

    db = SessionLocal()

    try:
        report = Report(**data)
        db.add(report)
        db.commit()

    finally:
        db.close()


# ============================================================
# LOAD HIIT SESSIONS (USER FILTERED)
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
            data.pop("_sa_instance_state", None)
            result.append(data)

        return result

    finally:
        db.close()