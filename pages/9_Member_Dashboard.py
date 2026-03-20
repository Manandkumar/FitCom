# ============================================================
# FitCom - Member Dashboard (FINAL DB VERSION)
# ============================================================

import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

from sidebar import render_sidebar
render_sidebar()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 🔥 DB FUNCTIONS (FINAL)
from storage import (
    load_reports,
    save_report,
    delete_record,
    save_hiit_session,
    load_hiit_sessions
)

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
    st.warning("⚠️ No members found. Please add a report first.")
    st.stop()

# -------------------------------------------------------
# LOGIN
# -------------------------------------------------------

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

    if st.button("Login"):

        if not selected_name:
            st.warning("Please select your name")

        elif password != selected_name:
            st.error("❌ Incorrect password")

        else:
            st.session_state.logged_in = True
            st.session_state.user = selected_name
            st.rerun()

# -------------------------------------------------------
# DASHBOARD
# -------------------------------------------------------

else:

    selected_name = st.session_state.user

    st.success(f"Welcome {selected_name} 👋")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    # -------------------------------------------------------
    # LOAD USER DATA
    # -------------------------------------------------------

    user_data = reports[selected_name]
    df = pd.DataFrame(user_data)

    if df.empty:
        st.info("No reports available")
        st.stop()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.sort_values("Date")

    df_display = df.drop(columns=["Age"], errors="ignore")
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
    # ADD PROGRESS (WITH DATE INPUT)
    # -------------------------------------------------------

    st.divider()
    st.subheader("➕ Add New Progress")

    progress_date = st.date_input("Select Progress Date", value=datetime.today())

    col1, col2 = st.columns(2)

    with col1:
        weight = st.number_input("Weight (kg)", 30.0, 200.0)
        bodyfat = st.number_input("Body Fat %", 1.0, 60.0)
        muscle_mass = st.number_input("Muscle Mass (kg)", 10.0, 100.0)

    with col2:
        body_water = st.number_input("Body Water %", 1.0, 80.0)
        visceral_fat = st.number_input("Visceral Fat", 1.0, 30.0)
        subcutaneous_fat = st.number_input("Subcutaneous Fat %", 1.0, 50.0)

    if st.button("Save Progress"):

        new_record = {
            "Name": selected_name,
            "Date": progress_date.strftime("%Y-%m-%d"),
            "Height": float(height),
            "Gender": gender,
            "Weight": float(weight),
            "BodyFat": float(bodyfat),
            "MuscleMass": float(muscle_mass),
            "BodyWater": float(body_water),
            "VisceralFat": float(visceral_fat),
            "SubcutaneousFat": float(subcutaneous_fat)
        }

        save_report(selected_name, new_record)

        st.success("✅ Progress saved!")
        st.rerun()

    # -------------------------------------------------------
    # PROGRESS CHARTS
    # -------------------------------------------------------

    st.subheader("📈 Progress")

    if "Weight" in df.columns:
        st.line_chart(df.set_index("Date")["Weight"])

    if "BodyFat" in df.columns:
        st.line_chart(df.set_index("Date")["BodyFat"])

    if "MuscleMass" in df.columns:
        st.line_chart(df.set_index("Date")["MuscleMass"])

    # -------------------------------------------------------
    # HIIT TRACKER (DB VERSION)
    # -------------------------------------------------------

    st.divider()
    st.subheader("🔥 HIIT Workout Tracker")

    with st.form("hiit_form"):

        hiit_date = st.date_input("Workout Date", value=datetime.today())

        col1, col2 = st.columns(2)

        with col1:
            workout_type = st.selectbox(
                "Workout Type",
                ["Running", "Cycling", "Skipping", "Circuit", "Other"]
            )
            duration = st.number_input("Duration (minutes)", 1, 180)

        with col2:
            calories = st.number_input("Calories Burned", 0)
            heart_rate = st.number_input("Avg Heart Rate", 0)

        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Save HIIT Session")

        if submitted:

            hiit_record = {
                "Name": selected_name,
                "Date": hiit_date.strftime("%Y-%m-%d"),
                "Workout": workout_type,
                "Duration": int(duration),
                "Calories": int(calories),
                "HeartRate": int(heart_rate),
                "Notes": notes
            }

            save_hiit_session(hiit_record)

            st.success("🔥 HIIT session saved!")
            st.rerun()

    # -------------------------------------------------------
    # HIIT HISTORY (DB)
    # -------------------------------------------------------

    st.subheader("📊 HIIT History")

    hiit_data = load_hiit_sessions(selected_name)

    if hiit_data:

        hiit_df = pd.DataFrame(hiit_data)

        hiit_df["Date"] = pd.to_datetime(hiit_df["Date"], errors="coerce")
        hiit_df = hiit_df.sort_values("Date", ascending=False)

        st.dataframe(hiit_df, use_container_width=True)

        # HIIT Trend
        if "Calories" in hiit_df.columns:
            st.subheader("📈 HIIT Calories Trend")
            st.line_chart(hiit_df.set_index("Date")["Calories"])

    else:
        st.info("No HIIT sessions yet")

    # -------------------------------------------------------
    # DELETE RECORD (SOFT DELETE)
    # -------------------------------------------------------

    st.subheader("🗑️ Delete Record")

    options = [
        f"{i} | {row.get('Date','')} | {row.get('Weight','')} kg"
        for i, row in df.iterrows()
    ]

    selected_index = st.selectbox(
        "Select record",
        range(len(options)),
        format_func=lambda x: options[x]
    )

    confirm = st.checkbox("Confirm delete")

    if st.button("Delete Selected Record"):

        if confirm:
            delete_record(selected_name, selected_index)
            st.success("🗑️ Record deleted!")
            st.rerun()
        else:
            st.warning("Please confirm deletion")