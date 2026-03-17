# ============================================================
# FitCom - Member Dashboard (With Add Progress)
# ============================================================

import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from storage import load_reports, save_report

st.title("👤 Member Dashboard")

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

reports = load_reports()

if not reports:
    st.warning("⚠️ No members found. Please add a report first.")
    st.stop()

# -------------------------------------------------------
# Login
# -------------------------------------------------------

st.subheader("🔐 Login")

member_names = sorted(list(reports.keys()))

selected_name = st.selectbox(
    "Select Member",
    member_names,
    index=None,
    placeholder="Choose your name..."
)

password = st.text_input("Enter Password", type="password")

# -------------------------------------------------------
# Login Logic
# -------------------------------------------------------

if st.button("Login"):

    if not selected_name:
        st.warning("Please select your name")

    elif password != selected_name:
        st.error("❌ Incorrect password")

    else:
        st.success(f"Welcome {selected_name} 👋")

        user_data = reports[selected_name]
        df = pd.DataFrame(user_data)

        # -------------------------------------------------------
        # Latest Profile (LOCKED FIELDS)
        # -------------------------------------------------------

        latest = df.iloc[-1]

        height = latest.get("Height", 0)
        gender = latest.get("Gender", "Male")
        age = latest.get("Age", 25)

        # -------------------------------------------------------
        # Show Stats
        # -------------------------------------------------------

        st.subheader("📊 Latest Stats")

        col1, col2, col3 = st.columns(3)

        col1.metric("Weight", f"{latest.get('Weight', 0)} kg")
        col2.metric("Body Fat", f"{latest.get('BodyFat', 0)} %")
        col3.metric("Muscle Mass", f"{latest.get('MuscleMass', 0)} kg")

        # -------------------------------------------------------
        # Add New Record (🔥 MAIN FEATURE)
        # -------------------------------------------------------

        st.divider()
        st.subheader("➕ Add New Progress")

        col1, col2 = st.columns(2)

        with col1:
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0)
            bodyfat = st.number_input("Body Fat %", min_value=1.0, max_value=60.0)
            muscle_mass = st.number_input("Muscle Mass (kg)", min_value=10.0, max_value=100.0)

        with col2:
            body_water = st.number_input("Body Water %", min_value=1.0, max_value=80.0)
            visceral_fat = st.number_input("Visceral Fat", min_value=1.0, max_value=30.0)
            subcutaneous_fat = st.number_input("Subcutaneous Fat %", min_value=1.0, max_value=50.0)

        if st.button("Save Progress"):

            new_record = {
                "Name": selected_name,
                "Date": datetime.now().strftime("%Y-%m-%d"),

                # Locked fields
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
            st.rerun()

        # -------------------------------------------------------
        # Charts
        # -------------------------------------------------------

        st.subheader("📈 Progress")

        if "Weight" in df.columns:
            st.line_chart(df["Weight"])

        if "BodyFat" in df.columns:
            st.line_chart(df["BodyFat"])

        if "MuscleMass" in df.columns:
            st.line_chart(df["MuscleMass"])

        # -------------------------------------------------------
        # Full Data
        # -------------------------------------------------------

        st.subheader("📋 Full Report")
        st.dataframe(df, use_container_width=True)