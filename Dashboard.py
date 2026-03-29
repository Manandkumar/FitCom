# ============================================================
# FitCom - Main Dashboard (FINAL STABLE VERSION)
# ============================================================

import streamlit as st
import pandas as pd
import os

from sidebar import render_sidebar
from storage import load_reports, load_hiit_sessions

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------

st.set_page_config(
    page_title="FitCom",
    page_icon="🏋️",
    layout="wide"
)

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

render_sidebar()

# ------------------------------------------------------------
# FITNESS SCORE FUNCTION
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
# LOAD REPORT DATA (DB)
# ------------------------------------------------------------

data = load_reports()

if not data:
    st.title("📊 FitCom Dashboard")
    st.info("No reports available yet.")
    st.stop()

df = pd.DataFrame(
    [item for sublist in data.values() for item in sublist]
)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])

# ------------------------------------------------------------
# DASHBOARD TITLE
# ------------------------------------------------------------

st.title("📊 FitCom Dashboard")

# ------------------------------------------------------------
# USER SELECTION
# ------------------------------------------------------------

user = st.selectbox(
    "Select User",
    sorted(df["Name"].dropna().unique())
)

user_df = df[df["Name"] == user].sort_values("Date")

latest = user_df.iloc[-1]

# ------------------------------------------------------------
# PROFILE + METRICS
# ------------------------------------------------------------

col1, col2 = st.columns([1, 3])

with col1:

    photo = latest.get("Photo", None)

    # ✅ FIXED IMAGE HANDLING (URL + PATH + BINARY)
    if photo:
        try:
            # Case 1: URL
            if isinstance(photo, str) and photo.startswith("http"):
                st.image(photo, width=150)

            # Case 2: Local file path
            elif isinstance(photo, str) and os.path.exists(photo):
                st.image(photo, width=150)

            # Case 3: Binary image (DB stored)
            elif isinstance(photo, (bytes, bytearray)):
                st.image(photo, width=150)

            else:
                st.image("https://via.placeholder.com/150", width=150)

        except Exception:
            st.image("https://via.placeholder.com/150", width=150)

    else:
        st.image("https://via.placeholder.com/150", width=150)

    st.write(f"**Name:** {latest.get('Name','')}")
    st.write(f"**Date:** {latest.get('Date','').strftime('%Y-%m-%d')}")

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
# USER HISTORY
# ------------------------------------------------------------

st.subheader("User History")
st.dataframe(user_df, use_container_width=True)

# ------------------------------------------------------------
# PROGRESS CHART
# ------------------------------------------------------------

if len(user_df) > 1:

    st.subheader("Progress Chart")

    available_cols = [
        col for col in ["Weight", "BodyFat", "MuscleMass"]
        if col in user_df.columns
    ]

    if available_cols:
        st.line_chart(user_df.set_index("Date")[available_cols])

# ============================================================
# 🔥 HIIT DASHBOARD SECTION
# ============================================================

st.subheader("🔥 HIIT Activity")

hiit_data = load_hiit_sessions(user)

if hiit_data:

    hiit_df = pd.DataFrame(hiit_data)

    hiit_df["Date"] = pd.to_datetime(hiit_df["Date"], errors="coerce")
    hiit_df = hiit_df.sort_values("Date", ascending=False)

    latest_hiit = hiit_df.iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("Last Workout", latest_hiit.get("Workout", "NA"))
    col2.metric("Calories Burned", latest_hiit.get("Calories", 0))
    col3.metric("Duration (min)", latest_hiit.get("Duration", 0))

    if "Calories" in hiit_df.columns:
        st.subheader("📈 Calories Burn Trend")
        st.line_chart(hiit_df.set_index("Date")["Calories"])

else:
    st.info("No HIIT sessions available")

# ------------------------------------------------------------
# MOST IMPROVED ATHLETE
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