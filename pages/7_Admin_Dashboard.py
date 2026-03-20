# ============================================================
# FitCom - Admin Dashboard (DB VERSION - STABLE)
# ============================================================

import streamlit as st
import pandas as pd

from storage import load_reports, update_record, delete_record
from sidebar import render_sidebar

render_sidebar()

ADMIN_CODE = "syntra123"

st.title("🛠️ Admin Dashboard")

# ------------------------------------------------------------
# ACCESS CONTROL
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
# LOAD DATA (DB)
# ------------------------------------------------------------

data = load_reports()

if not data:
    st.warning("No reports available.")
    st.stop()

# Flatten DB data
df = pd.DataFrame(
    [item for sublist in data.values() for item in sublist]
)

# ------------------------------------------------------------
# SYSTEM STATISTICS
# ------------------------------------------------------------

st.subheader("📊 System Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Athletes", df["Name"].nunique())
col2.metric("Total Reports", len(df))
col3.metric("Latest Entry", df["Date"].max())

# ------------------------------------------------------------
# DATA TABLE (EDITABLE)
# ------------------------------------------------------------

st.subheader("📋 All Reports")

edited_df = st.data_editor(df, use_container_width=True)

if st.button("Save Changes"):

    try:
        for _, row in edited_df.iterrows():
            update_record(
                row["Name"],
                row["Date"],
                row.to_dict()
            )

        st.success("Changes saved successfully ✅")

    except Exception as e:
        st.error(f"Update failed: {e}")

# ------------------------------------------------------------
# DELETE REPORT
# ------------------------------------------------------------

st.subheader("🗑 Delete Report")

user = st.selectbox("Select Athlete", sorted(df["Name"].dropna().unique()))

user_df = df[df["Name"] == user]

if not user_df.empty:

    date = st.selectbox("Select Date", sorted(user_df["Date"]))

    if st.button("Delete Selected Report"):

        # Find index within user's records
        user_records = df[df["Name"] == user].reset_index(drop=True)
        index = user_records[user_records["Date"] == date].index[0]

        delete_record(user, index)

        st.warning("Report deleted 🗑️")
        st.rerun()

# ------------------------------------------------------------
# DOWNLOAD DATA
# ------------------------------------------------------------

st.subheader("⬇️ Export Data")

st.download_button(
    "Download CSV",
    data=df.to_csv(index=False),
    file_name="fitcom_reports_backup.csv",
    mime="text/csv"
)