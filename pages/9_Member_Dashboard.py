# ============================================================
# FitCom - Member Dashboard (Final Version)
# ============================================================

import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# -------------------------------------------------------
# Fix Import Path (for pages folder access)
# -------------------------------------------------------

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from storage import load_reports, save_report

# -------------------------------------------------------
# Session State Initialization
# -------------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# -------------------------------------------------------
# Page Title
# -------------------------------------------------------

st.title("👤 Member Dashboard")

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

reports = load_reports()

if not reports:
    st.warning("⚠️ No members found. Please add a report first.")
    st.stop()

# -------------------------------------------------------
# Login Section (Only if not logged in)
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
            # Save login state
            st.session_state.logged_in = True
            st.session_state.user = selected_name

            st.rerun()

# -------------------------------------------------------
# Dashboard (After Login)
# -------------------------------------------------------

else:

    selected_name = st.session_state.user

    st.success(f"Welcome {selected_name} 👋")

    # Logout Button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    # -------------------------------------------------------
    # Load User Data
    # -------------------------------------------------------

    user_data = reports[selected_name]
    df = pd.DataFrame(user_data)

    if df.empty:
        st.info("No reports available")
        st.stop()

    # -------------------------------------------------------
    # Get Latest Profile (LOCKED FIELDS)
    # -------------------------------------------------------

    latest = df.iloc[-1]

    height = latest.get("Height", 0)
    gender = latest.get("Gender", "Male")
    age = latest.get("Age", 25)

    # -------------------------------------------------------
    # Show Latest Stats
    # -------------------------------------------------------

    st.subheader("📊 Latest Stats")

    col1, col2, col3 = st.columns(3)

    col1.metric("Weight", f"{latest.get('Weight', 0)} kg")
    col2.metric("Body Fat", f"{latest.get('BodyFat', 0)} %")
    col3.metric("Muscle Mass", f"{latest.get('MuscleMass', 0)} kg")

    # -------------------------------------------------------
    # Add New Progress (User Input)
    # -------------------------------------------------------

    st.divider()
    st.subheader("➕ Add New Progress")

    col1, col2 = st.columns(2)

    with col1:
        weight = st.number_input("Weight (kg)", 30.0, 200.0)
        bodyfat = st.number_input("Body Fat %", 1.0, 60.0)
        muscle_mass = st.number_input("Muscle Mass (kg)", 10.0, 100.0)

    with col2:
        body_water = st.number_input("Body Water %", 1.0, 80.0)
        visceral_fat = st.number_input("Visceral Fat", 1.0, 30.0)
        subcutaneous_fat = st.number_input("Subcutaneous Fat %", 1.0, 50.0)

    # -------------------------------------------------------
    # Save Progress
    # -------------------------------------------------------

    if st.button("Save Progress"):

        new_record = {
            "Name": selected_name,
            "Date": datetime.now().strftime("%Y-%m-%d"),

            # Locked fields (auto-filled)
            "Height": height,
            "Gender": gender,
            "Age": age,

            # New inputs
            "Weight": weight,
            "BodyFat": bodyfat,
            "MuscleMass": muscle_mass,
            "BodyWater": body_water,
            "VisceralFat": visceral_fat,
            "SubcutaneousFat": subcutaneous_fat
        }

        save_report(selected_name, new_record)

        st.success("✅ Progress saved successfully!")

        # Auto refresh UI
        st.rerun()

    # -------------------------------------------------------
    # Progress Charts
    # -------------------------------------------------------

    st.subheader("📈 Progress")

    if "Weight" in df.columns:
        st.line_chart(df["Weight"])

    if "BodyFat" in df.columns:
        st.line_chart(df["BodyFat"])

    if "MuscleMass" in df.columns:
        st.line_chart(df["MuscleMass"])

    # -------------------------------------------------------
    # Weekly AI Insights
    # -------------------------------------------------------

    def generate_insights(df):

        if len(df) < 2:
            return ["Not enough data yet"]

        insights = []

        recent = df.tail(7)

        # Weight trend
        weight_change = recent["Weight"].iloc[-1] - recent["Weight"].iloc[0]

        if weight_change < -1:
            insights.append("🔥 Great fat loss this week")
        elif weight_change > 1:
            insights.append("⚠️ Weight increased - review diet")
        else:
            insights.append("👍 Weight stable")

        # Body fat trend
        if "BodyFat" in recent:
            bf_change = recent["BodyFat"].iloc[-1] - recent["BodyFat"].iloc[0]

            if bf_change < -1:
                insights.append("💪 Body fat decreasing")
            elif bf_change > 1:
                insights.append("⚠️ Body fat increased")

        # Muscle trend
        if "MuscleMass" in recent:
            muscle_change = recent["MuscleMass"].iloc[-1] - recent["MuscleMass"].iloc[0]

            if muscle_change > 0:
                insights.append("🏋️ Muscle gain detected")
            elif muscle_change < 0:
                insights.append("⚠️ Muscle loss - increase protein")

        return insights

    st.subheader("🧠 Weekly Insights")

    for insight in generate_insights(df):
        st.info(insight)

    # -------------------------------------------------------
    # Full Data Table
    # -------------------------------------------------------

    st.subheader("📋 Full Report")
    st.dataframe(df, use_container_width=True)