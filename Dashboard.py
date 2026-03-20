# ============================================================
# FitCom - Body Composition Analytics Platform (DB VERSION)
# ============================================================

from database import engine
from models import Base

# CREATE TABLES
Base.metadata.create_all(bind=engine)

import streamlit as st
import pandas as pd
import os

from sidebar import render_sidebar
from storage import load_reports

# ✅ CRITICAL (creates tables)
from database import engine
from models import Base
Base.metadata.create_all(bind=engine)

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="FitCom",
    page_icon="🏋️",
    layout="wide"
)

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------

render_sidebar()

# ------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------

def calculate_fitness_score(row):

    score = 100

    if row.get("BMI", 0) > 25:
        score -= (row["BMI"] - 25) * 2

    if row.get("BodyFat", 0) > 20:
        score -= (row["BodyFat"] - 20) * 1.5

    if row.get("VisceralFat", 0) > 10:
        score -= (row["VisceralFat"] - 10) * 2

    if row.get("BodyWater", 50) < 50:
        score -= (50 - row["BodyWater"]) * 1.5

    return max(0, round(score))


# ------------------------------------------------------------
# LOAD DATA (DB)
# ------------------------------------------------------------

data = load_reports()

if not data:
    st.title("📊 FitCom Dashboard")
    st.info("No reports available yet.")
    st.stop()

# Flatten DB → DataFrame
df = pd.DataFrame(
    [item for sublist in data.values() for item in sublist]
)

# Fix date
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])

# ============================================================
# DASHBOARD
# ============================================================

st.title("📊 FitCom Dashboard")

# ------------------------------------------------------------
# Select User
# ------------------------------------------------------------

user = st.selectbox(
    "Select User",
    sorted(df["Name"].dropna().unique())
)

user_df = df[df["Name"] == user].sort_values("Date")

latest = user_df.iloc[-1]

# ------------------------------------------------------------
# Profile + Metrics
# ------------------------------------------------------------

col1, col2 = st.columns([1, 3])

with col1:

    photo = latest.get("Photo", None)

    if photo and isinstance(photo, str) and os.path.exists(photo):
        st.image(photo, width=150)

    st.write(f"**Name:** {latest.get('Name','')}")
    st.write(f"**Date:** {latest.get('Date','')}")

with col2:

    st.subheader("Latest Body Metrics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("BMI", latest.get("BMI", "NA"))
    c2.metric("Body Fat %", latest.get("BodyFat", "NA"))
    c3.metric("Muscle Mass", latest.get("MuscleMass", "NA"))
    c4.metric("Visceral Fat", latest.get("VisceralFat", "NA"))

    score = calculate_fitness_score(latest)

    st.subheader("Fitness Score")

    st.progress(score / 100)
    st.metric("Score", f"{score}/100")

# ------------------------------------------------------------
# User History
# ------------------------------------------------------------

st.subheader("User History")

st.dataframe(user_df, use_container_width=True)

# ------------------------------------------------------------
# Progress Chart
# ------------------------------------------------------------

if len(user_df) > 1:

    st.subheader("Progress Chart")

    available_cols = [
        col for col in ["Weight", "BodyFat", "MuscleMass"]
        if col in user_df.columns
    ]

    if available_cols:
        st.line_chart(user_df.set_index("Date")[available_cols])

# ------------------------------------------------------------
# Most Improved Athlete
# ------------------------------------------------------------

st.subheader("🔥 Most Improved Athlete")

improvements = []

for athlete in df["Name"].unique():

    athlete_df = df[df["Name"] == athlete].sort_values("Date")

    if len(athlete_df) > 1:

        start_fat = athlete_df.iloc[0].get("BodyFat", 0)
        end_fat = athlete_df.iloc[-1].get("BodyFat", 0)

        improvement = start_fat - end_fat

        improvements.append({
            "Name": athlete,
            "FatLoss": improvement
        })

if improvements:

    imp_df = pd.DataFrame(improvements)

    best = imp_df.sort_values("FatLoss", ascending=False).iloc[0]

    st.success(
        f"🏆 {best['Name']} improved the most with {round(best['FatLoss'],2)}% body fat reduction."
    )

else:
    st.info("Add multiple reports to calculate improvement.")


# ------------------------------------------------------------
# DEBUG (OPTIONAL - REMOVE LATER)
# ------------------------------------------------------------

st.write("Current working dir:", os.getcwd())

db_path = os.path.abspath("fitcom.db")
st.write("Expected DB path:", db_path)
st.write("Exists?", os.path.exists(db_path))