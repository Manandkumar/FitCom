# ============================================================
# FitCom - Member Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import sys
import os

# -------------------------------------------------------
# FIX IMPORT PATH (IMPORTANT)
# -------------------------------------------------------

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from storage import load_reports

# -------------------------------------------------------
# UI
# -------------------------------------------------------

st.title("👤 Member Dashboard")

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

reports = load_reports()

# DEBUG (uncomment if needed)
# st.write("DEBUG:", reports)

# -------------------------------------------------------
# Handle Empty Case
# -------------------------------------------------------

if not reports:
    st.warning("⚠️ No members found. Please add a report first.")
    st.stop()

# -------------------------------------------------------
# Login Section
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

login = st.button("Login")

# -------------------------------------------------------
# Login Logic
# -------------------------------------------------------

if login:

    if not selected_name:
        st.warning("Please select your name")

    elif password != selected_name:
        st.error("❌ Incorrect password")

    else:
        st.success(f"Welcome {selected_name} 👋")

        user_data = reports[selected_name]

        df = pd.DataFrame(user_data)

        if df.empty:
            st.info("No reports available")
        else:

            # -------------------------------------------------------
            # Latest Stats
            # -------------------------------------------------------

            latest = df.iloc[-1]

            st.subheader("📊 Latest Stats")

            col1, col2, col3 = st.columns(3)

            col1.metric("Weight", f"{latest.get('Weight', 0)} kg")
            col2.metric("Body Fat", f"{latest.get('BodyFat', 0)} %")
            col3.metric("Muscle Mass", f"{latest.get('MuscleMass', 0)} kg")

            # -------------------------------------------------------
            # Charts
            # -------------------------------------------------------

            st.subheader("📈 Progress")

            if "Weight" in df.columns:
                st.write("Weight Trend")
                st.line_chart(df["Weight"])

            if "BodyFat" in df.columns:
                st.write("Body Fat Trend")
                st.line_chart(df["BodyFat"])

            if "MuscleMass" in df.columns:
                st.write("Muscle Mass Trend")
                st.line_chart(df["MuscleMass"])

            # -------------------------------------------------------
            # Full Data Table
            # -------------------------------------------------------

            st.subheader("📋 Full Report")
            st.dataframe(df, use_container_width=True)