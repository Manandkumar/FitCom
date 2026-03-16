import streamlit as st
import pandas as pd
import os
from sidebar import render_sidebar

render_sidebar()

FILE_NAME = "fitcom_reports.csv"
ADMIN_CODE = "syntra123"

st.title("🛠️ Admin Dashboard")

# ------------------------------------------------------------
# Access Control
# ------------------------------------------------------------

if "admin_access" not in st.session_state:
    st.session_state.admin_access = False

if not st.session_state.admin_access:

    code = st.text_input("Enter Admin Access Code", type="password")

    if st.button("Unlock Dashboard"):

        if code == ADMIN_CODE:
            st.session_state.admin_access = True
            st.success("Admin access granted")
        else:
            st.error("Invalid access code")

    st.stop()

# ------------------------------------------------------------
# Load Data
# ------------------------------------------------------------

if not os.path.exists(FILE_NAME):
    st.warning("No reports available.")
    st.stop()

df = pd.read_csv(FILE_NAME)

# ------------------------------------------------------------
# System Statistics
# ------------------------------------------------------------

st.subheader("📊 System Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Athletes", df["Name"].nunique())
col2.metric("Total Reports", len(df))
col3.metric("Latest Entry", df["Date"].max())

# ------------------------------------------------------------
# Data Table
# ------------------------------------------------------------

st.subheader("📋 All Reports")

edited_df = st.data_editor(df, use_container_width=True)

if st.button("Save Changes"):
    edited_df.to_csv(FILE_NAME, index=False)
    st.success("Changes saved successfully")

# ------------------------------------------------------------
# Delete Report
# ------------------------------------------------------------

st.subheader("🗑 Delete Report")

user = st.selectbox("Select Athlete", df["Name"].unique())

user_df = df[df["Name"] == user]

date = st.selectbox("Select Date", user_df["Date"])

if st.button("Delete Selected Report"):

    df = df[~((df["Name"] == user) & (df["Date"] == date))]

    df.to_csv(FILE_NAME, index=False)

    st.warning("Report deleted")

# ------------------------------------------------------------
# Download Data
# ------------------------------------------------------------

st.subheader("⬇️ Export Data")

st.download_button(
    "Download CSV",
    data=df.to_csv(index=False),
    file_name="fitcom_reports_backup.csv",
    mime="text/csv"
)