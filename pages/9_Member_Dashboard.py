# ============================================================
# FitCom - Member Dashboard (FINAL WITH AUTH + STREAK 🔥)
# ============================================================

import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

from sidebar import render_sidebar
render_sidebar()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from storage import (
    load_reports,
    save_report,
    delete_record,
    save_hiit_session,
    load_hiit_sessions,
    get_user_password,
    set_user_password,
    hash_password
)

# -------------------------------------------------------
# 🔥 STREAK CALCULATION
# -------------------------------------------------------

def calculate_streaks(df):

    if df.empty:
        return 0, 0

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    dates = sorted(df["Date"].dt.date.unique())

    if not dates:
        return 0, 0

    current_streak = 1
    longest_streak = 1

    for i in range(1, len(dates)):
        diff = (dates[i] - dates[i - 1]).days

        if diff == 1:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1

    if (datetime.today().date() - dates[-1]).days > 1:
        current_streak = 0

    return current_streak, longest_streak


# -------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# -------------------------------------------------------
# PAGE TITLE
# -------------------------------------------------------

st.title("👤 Member Dashboard")

reports = load_reports()

if not reports:
    st.warning("⚠️ No members found.")
    st.stop()


# =======================================================
# 🔐 LOGIN SYSTEM (FINAL)
# =======================================================

if not st.session_state.logged_in:

    st.subheader("🔐 Login")

    member_names = sorted(list(reports.keys()))

    selected_name = st.selectbox(
        "Select Member",
        member_names,
        index=None,
        placeholder="Choose your name..."
    )

    password = st.text_input("Enter Password", type="password")

    if selected_name:

        stored_password = get_user_password(selected_name)

        # ---------------------------
        # FIRST TIME PASSWORD SETUP
        # ---------------------------
        if not stored_password:

            st.warning("⚠️ First time login — set your password")

            new_pass = st.text_input("Set Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")

            if st.button("Create Password"):

                if not new_pass:
                    st.warning("Enter password")

                elif new_pass != confirm_pass:
                    st.error("Passwords do not match")

                else:
                    set_user_password(selected_name, new_pass)
                    st.success("✅ Password created! Login again.")
                    st.rerun()

        # ---------------------------
        # NORMAL LOGIN
        # ---------------------------
        else:

            if st.button("Login"):

                if hash_password(password) != stored_password:
                    st.error("❌ Incorrect password")

                else:
                    st.session_state.logged_in = True
                    st.session_state.user = selected_name
                    st.success("Login successful ✅")
                    st.rerun()


# =======================================================
# DASHBOARD
# =======================================================

else:

    selected_name = st.session_state.user

    st.success(f"Welcome {selected_name} 👋")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    # -------------------------------------------------------
    # CHANGE PASSWORD
    # -------------------------------------------------------

    st.divider()
    st.subheader("🔐 Change Password")

    current_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Update Password"):

        stored_password = get_user_password(selected_name)

        if hash_password(current_password) != stored_password:
            st.error("❌ Current password incorrect")

        elif new_password != confirm_password:
            st.error("Passwords do not match")

        else:
            set_user_password(selected_name, new_password)
            st.success("✅ Password updated")

    # -------------------------------------------------------
    # LOAD USER DATA
    # -------------------------------------------------------

    user_data = reports[selected_name]
    df = pd.DataFrame(user_data)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.sort_values("Date")

    latest = df.iloc[-1]

    height = latest.get("Height", 0)
    gender = latest.get("Gender", "Male")

    # -------------------------------------------------------
    # CURRENT STATS
    # -------------------------------------------------------

    st.subheader("📊 Latest Stats")

    col1, col2, col3 = st.columns(3)

    col1.metric("Weight", f"{latest.get('Weight', 0)} kg")
    col2.metric("Body Fat", f"{latest.get('BodyFat', 0)} %")
    col3.metric("Muscle Mass", f"{latest.get('MuscleMass', 0)} kg")

    # -------------------------------------------------------
    # ADD PROGRESS
    # -------------------------------------------------------

    st.divider()
    st.subheader("➕ Add Progress")

    progress_date = st.date_input("Date", value=datetime.today())

    weight = st.number_input("Weight", 30.0, 200.0)
    bodyfat = st.number_input("Body Fat", 1.0, 60.0)
    muscle_mass = st.number_input("Muscle Mass", 10.0, 100.0)

    if st.button("Save Progress"):

        save_report(selected_name, {
            "Name": selected_name,
            "Date": progress_date.strftime("%Y-%m-%d"),
            "Height": height,
            "Gender": gender,
            "Weight": weight,
            "BodyFat": bodyfat,
            "MuscleMass": muscle_mass
        })

        st.success("Saved!")
        st.rerun()

    # -------------------------------------------------------
    # PROGRESS
    # -------------------------------------------------------

    st.subheader("📈 Progress")

    st.line_chart(df.set_index("Date")[["Weight", "BodyFat", "MuscleMass"]])

    # -------------------------------------------------------
    # HIIT
    # -------------------------------------------------------

    st.subheader("🔥 HIIT Tracker")

    with st.form("hiit"):

        hiit_date = st.date_input("Workout Date", datetime.today())
        workout = st.selectbox("Workout", ["Run", "Cycle", "HIIT"])
        calories = st.number_input("Calories", 0)

        if st.form_submit_button("Save"):

            save_hiit_session({
                "Name": selected_name,
                "Date": hiit_date.strftime("%Y-%m-%d"),
                "Workout": workout,
                "Calories": calories
            })

            st.success("Saved!")
            st.rerun()

    hiit_data = load_hiit_sessions(selected_name)

    if hiit_data:

        hiit_df = pd.DataFrame(hiit_data)
        hiit_df["Date"] = pd.to_datetime(hiit_df["Date"])

        st.dataframe(hiit_df)

        # STREAK
        st.subheader("🔥 Streak")

        current, longest = calculate_streaks(hiit_df)

        col1, col2 = st.columns(2)
        col1.metric("Current", current)
        col2.metric("Best", longest)

    # -------------------------------------------------------
    # DELETE
    # -------------------------------------------------------

    st.subheader("🗑 Delete Record")

    idx = st.selectbox("Select", range(len(df)))

    if st.button("Delete"):
        delete_record(selected_name, idx)
        st.success("Deleted")
        st.rerun()