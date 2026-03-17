# ============================================================
# FitCom - Member Dashboard (Final Fixed Version)
# ============================================================

import streamlit as st
import pandas as pd
import sys
import os
from sidebar import render_sidebar

render_sidebar()
from datetime import datetime

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from storage import load_reports, save_report, delete_record

# -------------------------------------------------------
# Session State
# -------------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# -------------------------------------------------------
# UI
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

    user_data = reports[selected_name]
    df = pd.DataFrame(user_data)

    if df.empty:
        st.info("No reports available")
        st.stop()

    latest = df.iloc[-1]

    height = latest.get("Height", 0)
    gender = latest.get("Gender", "Male")
    age = latest.get("Age", 25)

    # -------------------------------------------------------
    # STATS
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

    if st.button("Save Progress"):

        new_record = {
            "Name": selected_name,
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Height": height,
            "Gender": gender,
            "Age": age,
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
    # CHARTS
    # -------------------------------------------------------

    st.subheader("📈 Progress")

    if "Weight" in df.columns:
        st.line_chart(df["Weight"])

    if "BodyFat" in df.columns:
        st.line_chart(df["BodyFat"])

    if "MuscleMass" in df.columns:
        st.line_chart(df["MuscleMass"])

    # -------------------------------------------------------
    # INSIGHTS
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
    # TABLE
    # -------------------------------------------------------

    st.subheader("📋 Full Report")
    st.dataframe(df, use_container_width=True)

    # -------------------------------------------------------
    # DELETE RECORD
    # -------------------------------------------------------

    st.subheader("🗑️ Delete Record")

    if len(df) > 0:

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