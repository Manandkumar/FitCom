# ============================================================
# Update Record
# ============================================================

import streamlit as st
import pandas as pd

from sidebar import render_sidebar
from storage import load_reports, save_report

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

def calc_score(bmi, fat, muscle, weight):
    score = 0
    if 18.5 <= bmi <= 24.9:
        score += 20
    if fat <= 25:
        score += 20
    if muscle >= 40:
        score += 15
    if weight <= 90:
        score += 10
    return score

score = calc_score(bmi, fat, muscle, weight)
st.metric("Score", score)

if st.button("Update"):

    rec["Weight"] = weight
    rec["BodyFat"] = fat
    rec["MuscleMass"] = muscle
    rec["BMI"] = bmi
    rec["HealthScore"] = score

    save_report(user, rec)

    st.success("Updated ✅")