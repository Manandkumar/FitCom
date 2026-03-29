# ============================================================
# FitCom - Database Operations (FINAL FIXED)
# ============================================================

from database import SessionLocal
from models import Report, HIITSession


# ============================================================
# LOAD REPORTS (USER)
# ============================================================

def load_reports():
    db = SessionLocal()

    try:
        import streamlit as st
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
            data.pop("_sa_instance_state", None)

            result.setdefault(r.UserId, []).append(data)

        return result

    finally:
        db.close()


# ============================================================
# SAVE REPORT
# ============================================================

def save_report(user, data):
    db = SessionLocal()

    try:
        report = Report(**data)
        db.add(report)
        db.commit()

    finally:
        db.close()


# ============================================================
# LOAD ALL REPORTS
# ============================================================

def load_all_reports():
    db = SessionLocal()

    try:
        reports = db.query(Report).filter(
            Report.IsDeleted == False
        ).all()

        result = []

        for r in reports:
            data = r.__dict__.copy()
            data.pop("_sa_instance_state", None)
            result.append(data)

        return result

    finally:
        db.close()


# ============================================================
# SAVE HIIT SESSION
# ============================================================

def save_hiit_session(data):
    db = SessionLocal()

    try:
        session = HIITSession(**data)
        db.add(session)
        db.commit()

    finally:
        db.close()


# ============================================================
# LOAD HIIT SESSIONS
# ============================================================

def load_hiit_sessions(user):
    db = SessionLocal()

    try:
        sessions = db.query(HIITSession).filter(
            HIITSession.UserId == user,
            HIITSession.IsDeleted == False
        ).all()

        result = []

        for s in sessions:
            d = s.__dict__.copy()
            d.pop("_sa_instance_state", None)
            result.append(d)

        return result

    finally:
        db.close()