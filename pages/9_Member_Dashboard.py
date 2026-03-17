# ============================================================
# FitCom - Member Dashboard
# ============================================================

import streamlit as st
import json
import pandas as pd
import os

st.title("👤 Member Dashboard")

# -------------------------------------------------------
# Load Reports (adjust if using database.py later)
# -------------------------------------------------------

def load_reports():
    if os.path.exists("data/reports.json"):
        with open("data/reports.json", "r") as f:
            return json.load(f)
    return {}

reports = load_reports()

# -------------------------------------------------------
# Dropdown Login
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

if st.button("Login"):

    if not selected_name:
        st.warning("Please select your name")

    elif password != selected_name:
        st.error("Incorrect password")

    else:
        st.success(f"Welcome {selected_name} 👋")

        user_data = reports[selected_name]
        df = pd.DataFrame(user_data)

        if df.empty:
            st.info("No reports available")
        else:

            latest = df.iloc[-1]

            st.subheader("📊 Latest Stats")

            col1, col2, col3 = st.columns(3)

            col1.metric("Weight", f"{latest.get('Weight', 0)} kg")
            col2.metric("Body Fat", f"{latest.get('BodyFat', 0)} %")
            col3.metric("Muscle", f"{latest.get('MuscleMass', 0)} kg")

            st.subheader("📈 Progress")

            if "Weight" in df.columns:
                st.line_chart(df["Weight"])

            if "BodyFat" in df.columns:
                st.line_chart(df["BodyFat"])

            if "MuscleMass" in df.columns:
                st.line_chart(df["MuscleMass"])

            st.subheader("📋 Full Data")
            st.dataframe(df, use_container_width=True)