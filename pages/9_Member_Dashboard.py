# ============================================================
# FitCom - Member Dashboard (FINAL FIXED AUTH 🔥)
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
# 🔐 LOGIN SYSTEM (FINAL FIX)
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

    if selected_name:

        stored_password = get_user_password(selected_name)

        # ---------------- FIRST TIME / BROKEN STATE ----------------
        if stored_password is None:

            st.warning("⚠️ First time / Reset login — set your password")

            new_pass = st.text_input("Set Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")

            if st.button("Create Password"):

                if not new_pass:
                    st.warning("Enter password")

                elif new_pass != confirm_pass:
                    st.error("Passwords do not match")

                else:
                    # 🔥 Save password
                    set_user_password(selected_name, new_pass)

                    # 🔥 HARD VERIFY (THIS IS THE KEY FIX)
                    verify = get_user_password(selected_name)

                    if verify is None:
                        st.error("❌ Password not saved. DB issue.")
                    else:
                        st.success("✅ Password created! Please login.")
                        st.rerun()

        # ---------------- NORMAL LOGIN ----------------
        else:

            password = st.text_input("Enter Password", type="password")

            if st.button("Login"):

                if not password:
                    st.warning("Enter password")

                else:
                    if hash_password(password) == stored_password:
                        st.session_state.logged_in = True
                        st.session_state.user = selected_name
                        st.success("Login successful ✅")
                        st.rerun()
                    else:
                        st.error("❌ Incorrect password")


# =======================================================
# 🏠 DASHBOARD
# =======================================================

else:

    selected_name = st.session_state.user

    st.success(f"Welcome {selected_name} 👋")

    colA, colB = st.columns([6, 1])

    with colB:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

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
            "Weight": float(weight),
            "BodyFat": float(bodyfat),
            "MuscleMass": float(muscle_mass)
        })

        st.success("Saved!")
        st.rerun()

    # -------------------------------------------------------
    # PROGRESS
    # -------------------------------------------------------

    st.subheader("📈 Progress")

    available_cols = [col for col in ["Weight", "BodyFat", "MuscleMass"] if col in df.columns]

    if available_cols:
        st.line_chart(df.set_index("Date")[available_cols])

    # -------------------------------------------------------
    # HIIT
    # -------------------------------------------------------

    st.subheader("🔥 HIIT Tracker")

    with st.form("hiit"):

        hiit_date = st.date_input("Workout Date", datetime.today())
        workout = st.selectbox("Workout", ["Run", "Cycle", "HIIT"])
        calories = st.number_input("Calories", 0)

        submitted = st.form_submit_button("Save")

        if submitted:

            save_hiit_session({
                "Name": selected_name,
                "Date": hiit_date.strftime("%Y-%m-%d"),
                "Workout": workout,
                "Calories": int(calories)
            })

            st.success("Saved!")
            st.rerun()

    hiit_data = load_hiit_sessions(selected_name)

    if hiit_data:

        hiit_df = pd.DataFrame(hiit_data)
        hiit_df["Date"] = pd.to_datetime(hiit_df["Date"], errors="coerce")

        st.dataframe(hiit_df.sort_values("Date", ascending=False))

        st.subheader("🔥 Workout Streak")

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