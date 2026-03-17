# ============================================================
# FitCom - Member Dashboard
# Author: Anand Kumar
#
# Notes:
# - Handles login + member-specific dashboard
# - Allows user to track progress over time
# - Age is intentionally hidden from UI (privacy)
# ============================================================

import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# -------------------------------------------------------
# Load shared sidebar (keeps UI consistent across pages)
# -------------------------------------------------------
from sidebar import render_sidebar
render_sidebar()

# Fix path so we can import modules from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from storage import load_reports, save_report, delete_record

# -------------------------------------------------------
# SESSION STATE (basic login persistence)
# -------------------------------------------------------
# Keeps user logged in across reruns

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# -------------------------------------------------------
# PAGE TITLE
# -------------------------------------------------------

st.title("👤 Member Dashboard")

# Load all reports (grouped by member name)
reports = load_reports()

# Safety check – no data available
if not reports:
    st.warning("⚠️ No members found. Please add a report first.")
    st.stop()

# -------------------------------------------------------
# LOGIN SECTION
# -------------------------------------------------------
# Very simple auth:
# Username = Name
# Password = Name (can be upgraded later)

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
            # Save login state
            st.session_state.logged_in = True
            st.session_state.user = selected_name
            st.rerun()

# -------------------------------------------------------
# MAIN DASHBOARD (AFTER LOGIN)
# -------------------------------------------------------

else:

    selected_name = st.session_state.user

    st.success(f"Welcome {selected_name} 👋")

    # Simple logout
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

    # -------------------------------------------------------
    # Hide sensitive fields (Age not shown in UI)
    # -------------------------------------------------------
    df_display = df.drop(columns=["Age"], errors="ignore")

    # Latest record (used for current stats)
    latest = df.iloc[-1]

    # Lock profile fields (should not change per entry)
    height = latest.get("Height", 0)
    gender = latest.get("Gender", "Male")

    # -------------------------------------------------------
    # CURRENT STATS (quick snapshot)
    # -------------------------------------------------------

    st.subheader("📊 Latest Stats")

    col1, col2, col3 = st.columns(3)

    col1.metric("Weight", f"{latest.get('Weight', 0)} kg")
    col2.metric("Body Fat", f"{latest.get('BodyFat', 0)} %")
    col3.metric("Muscle Mass", f"{latest.get('MuscleMass', 0)} kg")

    # -------------------------------------------------------
    # ADD NEW PROGRESS ENTRY
    # -------------------------------------------------------
    # Only dynamic metrics are entered (profile stays locked)

    st.divider()
    st.subheader("➕ Add New Progress")

    col1, col2 = st.columns(2)

    with col1:
        weight = st.number_input("Weight (kg)", 30.0, 200.0, key="weight")
        bodyfat = st.number_input("Body Fat %", 1.0, 60.0, key="bodyfat")
        muscle_mass = st.number_input("Muscle Mass (kg)", 10.0, 100.0, key="muscle")

    with col2:
        body_water = st.number_input("Body Water %", 1.0, 80.0, key="water")
        visceral_fat = st.number_input("Visceral Fat", 1.0, 30.0, key="visceral")
        subcutaneous_fat = st.number_input("Subcutaneous Fat %", 1.0, 50.0, key="subfat")

    # Save new progress entry
    if st.button("Save Progress"):

        new_record = {
            "Name": selected_name,
            "Date": datetime.now().strftime("%Y-%m-%d"),

            # Locked fields (carried forward)
            "Height": height,
            "Gender": gender,

            # Dynamic tracking fields
            "Weight": weight,
            "BodyFat": bodyfat,
            "MuscleMass": muscle_mass,
            "BodyWater": body_water,
            "VisceralFat": visceral_fat,
            "SubcutaneousFat": subcutaneous_fat
        }

        save_report(selected_name, new_record)

        st.success("✅ Progress saved!")
        st.rerun()

    # -------------------------------------------------------
    # PROGRESS CHARTS
    # -------------------------------------------------------
    # Simple trend tracking

    st.subheader("📈 Progress")

    if "Weight" in df.columns:
        st.line_chart(df["Weight"])

    if "BodyFat" in df.columns:
        st.line_chart(df["BodyFat"])

    if "MuscleMass" in df.columns:
        st.line_chart(df["MuscleMass"])

    # -------------------------------------------------------
    # WEEKLY INSIGHTS (basic logic for now)
    # -------------------------------------------------------

    st.subheader("🧠 Weekly Insights")

    if len(df) > 1:

        recent = df.tail(7)

        weight_change = recent["Weight"].iloc[-1] - recent["Weight"].iloc[0]

        if weight_change < -1:
            st.info("🔥 Great fat loss this week")
        elif weight_change > 1:
            st.warning("⚠️ Weight increased")
        else:
            st.info("👍 Weight stable")

    # -------------------------------------------------------
    # FULL DATA TABLE (Age hidden)
    # -------------------------------------------------------

    st.subheader("📋 Full Report")
    st.dataframe(df_display, use_container_width=True)

    # -------------------------------------------------------
    # DELETE RECORD
    # -------------------------------------------------------
    # Allows removing incorrect entries

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