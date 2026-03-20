# ============================================================
# FitCom - Edit Athlete Report (DB VERSION - STABLE)
# ============================================================

import streamlit as st
import pandas as pd

from storage import load_reports, update_record
from sidebar import render_sidebar

render_sidebar()

ADMIN_CODE = "syntra123"

st.title("✏️ Edit Athlete Report")

# ------------------------------------------------------------
# ACCESS CONTROL
# ------------------------------------------------------------

if "authorized" not in st.session_state:
    st.session_state.authorized = False

if not st.session_state.authorized:

    code = st.text_input("Enter Admin Access Code", type="password")

    if st.button("Unlock"):
        if code == ADMIN_CODE:
            st.session_state.authorized = True
            st.success("Access granted")
        else:
            st.error("Invalid access code")

    st.stop()

# ------------------------------------------------------------
# LOAD DATA (DB)
# ------------------------------------------------------------

data = load_reports()

if not data:
    st.info("No reports available to edit.")
    st.stop()

# Flatten data
df = pd.DataFrame(
    [item for sublist in data.values() for item in sublist]
)

# ------------------------------------------------------------
# SELECT USER
# ------------------------------------------------------------

user = st.selectbox("Select Athlete", sorted(df["Name"].dropna().unique()))

user_df = df[df["Name"] == user]

if user_df.empty:
    st.warning("No records found for selected athlete.")
    st.stop()

# ------------------------------------------------------------
# SELECT DATE
# ------------------------------------------------------------

date = st.selectbox("Select Report Date", sorted(user_df["Date"]))

record = user_df[user_df["Date"] == date].iloc[0]

# ------------------------------------------------------------
# EDIT FORM
# ------------------------------------------------------------

st.subheader("Edit Metrics")

weight = st.number_input("Weight", value=float(record.get("Weight", 0)))
bmi = st.number_input("BMI", value=float(record.get("BMI", 0)))
bodyfat = st.number_input("Body Fat", value=float(record.get("BodyFat", 0)))
muscle = st.number_input("Muscle Mass", value=float(record.get("MuscleMass", 0)))
visceral = st.number_input("Visceral Fat", value=float(record.get("VisceralFat", 0)))
water = st.number_input("Body Water", value=float(record.get("BodyWater", 0)))

# ------------------------------------------------------------
# UPDATE
# ------------------------------------------------------------

if st.button("Update Report"):

    try:
        update_record(user, date, {
            "Weight": float(weight),
            "BMI": float(bmi),
            "BodyFat": float(bodyfat),
            "MuscleMass": float(muscle),
            "VisceralFat": float(visceral),
            "BodyWater": float(water)
        })

        st.success("Report updated successfully! ✅")

    except Exception as e:
        st.error(f"Update failed: {e}")