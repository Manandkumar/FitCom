# ============================================================
# FitCom Dashboard (FINAL STABLE)
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sidebar import render_sidebar
from storage import load_reports
from storage.database_ops import load_hiit_sessions
from utils import calculate_health_score

st.set_page_config(layout="wide")
render_sidebar()

user = st.session_state.get("user")

if not user:
    st.error("Login required")
    st.stop()

st.title("🏠 My Fitness Dashboard")

# LOAD DATA
data = load_reports()

records = []
for _, entries in data.items():
    for r in entries:
        if not r.get("IsDeleted"):
            records.append(r)

if not records:
    st.info("No records")
    st.stop()

df = pd.DataFrame(records)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

latest = df.iloc[-1]

# HEALTH SCORE
score = latest.get("HealthScore")

if not score or score == 0:
    score, status = calculate_health_score(latest)
else:
    status = latest.get("HealthStatus", "")

# METRICS
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Weight", latest["Weight"])
col2.metric("BMI", latest["BMI"])
col3.metric("Body Fat", latest["BodyFat"])
col4.metric("Muscle", latest["MuscleMass"])
col5.metric("Health Score", score)

st.write(status)

# PHOTO
st.subheader("📸 Photo")

if latest.get("Photo"):
    st.image(latest["Photo"], width=250)

# HIIT
st.subheader("🔥 HIIT")

sessions = load_hiit_sessions(user)

if sessions:
    last = sessions[-1]
    st.write(f"Date: {last['Date']}")
    st.write(f"Workout: {last['Workout']}")
    st.write(f"Duration: {last['Duration']} mins")

# TRENDS
st.subheader("📈 Trends")

fig, ax = plt.subplots()
ax.plot(df["Date"], df["Weight"], marker='o')
st.pyplot(fig)

fig, ax = plt.subplots()
ax.plot(df["Date"], df["BMI"], marker='o')
st.pyplot(fig)

# HEALTH SCORE TREND
scores = []
for _, row in df.iterrows():
    s = row.get("HealthScore")
    if not s or s == 0:
        s, _ = calculate_health_score(row)
    scores.append(s)

df["Score"] = scores

fig, ax = plt.subplots()
ax.plot(df["Date"], df["Score"], marker='o')
st.pyplot(fig)

# TABLE
st.dataframe(df)