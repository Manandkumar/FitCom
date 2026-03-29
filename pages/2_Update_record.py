# ============================================================
# Update Record
# ============================================================

import streamlit as st
import pandas as pd

from sidebar import render_sidebar
from storage import load_reports, save_report
from utils import calculate_health_score

st.set_page_config(layout="wide")
render_sidebar()

st.title("✏️ Update Record")

user = st.session_state.get("user")

if not user:
    st.error("Login required")
    st.stop()

data = load_reports()

records = []
for _, entries in data.items():
    for r in entries:
        if not r.get("IsDeleted"):
            records.append(r)

df = pd.DataFrame(records)

if df.empty:
    st.info("No records")
    st.stop()

selected = st.selectbox("Select Date", df["Date"])

rec = df[df["Date"] == selected].iloc[0]

weight = st.number_input("Weight", value=float(rec["Weight"]))
fat = st.number_input("Body Fat", value=float(rec["BodyFat"]))
muscle = st.number_input("Muscle", value=float(rec["MuscleMass"]))

height = rec["Height"]
bmi = round(weight / ((height/100)**2), 2)

st.metric("BMI", bmi)

score, status = calculate_health_score({
    "BMI": bmi,
    "BodyFat": fat,
    "MuscleMass": muscle,
    "VisceralFat": rec.get("VisceralFat", 0),
    "BMR": rec.get("BMR", 0),
    "Weight": weight
})

st.metric("Health Score", score)

if st.button("Update"):

    rec["Weight"] = weight
    rec["BodyFat"] = fat
    rec["MuscleMass"] = muscle
    rec["BMI"] = bmi

    rec["HealthScore"] = score
    rec["HealthStatus"] = status

    save_report(user, rec)

    st.success("Updated ✅")