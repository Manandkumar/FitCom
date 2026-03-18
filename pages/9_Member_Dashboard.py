# ============================================================
# FitCom - Member Dashboard
# Author: Anand Kumar
#
# Description:
# - Member login system
# - Body composition tracking
# - Progress visualization
# - HIIT tracking (Add, View, Edit, Delete)
# ============================================================

import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# -------------------------------------------------------
# LOAD SIDEBAR
# -------------------------------------------------------
from sidebar import render_sidebar
render_sidebar()

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from storage import load_reports, save_report, delete_record

# -------------------------------------------------------
# HIIT STORAGE UTILITIES
# -------------------------------------------------------

HIIT_FILE = "hiit_data.csv"


def save_hiit_session(data):
    """Save HIIT session"""
    df = pd.DataFrame([data])

    if os.path.exists(HIIT_FILE):
        df.to_csv(HIIT_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(HIIT_FILE, index=False)


def load_hiit_sessions():
    """Load HIIT sessions"""
    if os.path.exists(HIIT_FILE):
        return pd.read_csv(HIIT_FILE)
    return pd.DataFrame()


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
    st.warning("⚠️ No members found. Add a report first.")
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

    st.subheader("📈 Progress")

    if "Weight" in df.columns:
        st.line_chart(df["Weight"])

    if "BodyFat" in df.columns:
        st.line_chart(df["BodyFat"])

    if "MuscleMass" in df.columns:
        st.line_chart(df["MuscleMass"])

    # -------------------------------------------------------
    # HIIT TRACKER
    # -------------------------------------------------------

    st.divider()
    st.subheader("🔥 HIIT Workout Tracker")

    with st.form("hiit_form"):

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
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Workout": workout_type,
                "Duration": duration,
                "Calories": calories,
                "HeartRate": heart_rate,
                "Notes": notes
            }

            save_hiit_session(hiit_record)

            st.success("🔥 HIIT session saved!")
            st.rerun()

    # -------------------------------------------------------
    # HIIT HISTORY
    # -------------------------------------------------------

    st.subheader("📊 HIIT History")

    hiit_df = load_hiit_sessions()

    if not hiit_df.empty:

        user_hiit = hiit_df[hiit_df["Name"] == selected_name]

        if not user_hiit.empty:
            st.dataframe(user_hiit.sort_index(ascending=False), use_container_width=True)
        else:
            st.info("No HIIT sessions yet")

    else:
        st.info("No HIIT data available")

    # -------------------------------------------------------
    # EDIT HIIT
    # -------------------------------------------------------

    st.subheader("✏️ Edit HIIT Session")

    if not hiit_df.empty:

        user_hiit = hiit_df[hiit_df["Name"] == selected_name].reset_index()

        if not user_hiit.empty:

            options = [
                f"{row['Date']} | {row['Workout']} | {row['Calories']} cal"
                for _, row in user_hiit.iterrows()
            ]

            selected_idx = st.selectbox(
                "Select session",
                range(len(options)),
                format_func=lambda x: options[x]
            )

            selected_row = user_hiit.iloc[selected_idx]

            with st.form("edit_hiit"):

                workout_type = st.selectbox(
                    "Workout",
                    ["Running", "Cycling", "Skipping", "Circuit", "Other"],
                    index=0
                )

                duration = st.number_input("Duration", value=int(selected_row["Duration"]))
                calories = st.number_input("Calories", value=int(selected_row["Calories"]))
                heart_rate = st.number_input("Heart Rate", value=int(selected_row["HeartRate"]))
                notes = st.text_area("Notes", value=selected_row.get("Notes", ""))

                if st.form_submit_button("Update"):

                    idx = selected_row["index"]

                    hiit_df.loc[idx, "Workout"] = workout_type
                    hiit_df.loc[idx, "Duration"] = duration
                    hiit_df.loc[idx, "Calories"] = calories
                    hiit_df.loc[idx, "HeartRate"] = heart_rate
                    hiit_df.loc[idx, "Notes"] = notes

                    hiit_df.to_csv(HIIT_FILE, index=False)

                    st.success("Updated successfully!")
                    st.rerun()

    # -------------------------------------------------------
    # DELETE HIIT
    # -------------------------------------------------------

    st.subheader("🗑️ Delete HIIT Session")

    if not hiit_df.empty:

        user_hiit = hiit_df[hiit_df["Name"] == selected_name].reset_index()

        if not user_hiit.empty:

            delete_idx = st.selectbox(
                "Select session to delete",
                range(len(user_hiit)),
                format_func=lambda x: f"{user_hiit.iloc[x]['Date']} | {user_hiit.iloc[x]['Workout']}"
            )

            confirm = st.checkbox("Confirm delete")

            if st.button("Delete HIIT"):

                if confirm:

                    idx = user_hiit.iloc[delete_idx]["index"]
                    hiit_df = hiit_df.drop(index=idx)

                    hiit_df.to_csv(HIIT_FILE, index=False)

                    st.success("Deleted successfully!")
                    st.rerun()
                else:
                    st.warning("Please confirm deletion")