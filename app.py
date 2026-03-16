# ============================================================
# FitCom - Body Composition Analytics Platform
# Author: Anand Kumar
# ============================================================

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from storage import save_report

FILE_NAME = "fitcom_reports.csv"

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="FitCom",
    page_icon="🏋️",
    layout="wide"
)

# ------------------------------------------------------------
# Hide Streamlit Default Pages Navigation
# ------------------------------------------------------------

st.markdown(
"""
<style>
[data-testid="stSidebarNav"] {display: none;}
</style>
""",
unsafe_allow_html=True
)

# ------------------------------------------------------------
# Sidebar Navigation
# ------------------------------------------------------------

# Sidebar Branding

st.sidebar.image("logo.png", width=160)
st.sidebar.title("FitCom")

page = st.sidebar.selectbox(
    "Navigate",
    ["Dashboard", "Add Report", "Progress", "Leaderboard", "AI Coach"]
)

# ------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------

def calculate_bmi(weight, height_in):

    if height_in == 0:
        return None

    height_m = height_in * 0.0254
    bmi = weight / (height_m ** 2)

    return round(bmi, 2)


def calculate_fitness_score(row):

    score = 100

    if row["BMI"] > 25:
        score -= (row["BMI"] - 25) * 2

    if row["BodyFat"] > 20:
        score -= (row["BodyFat"] - 20) * 1.5

    if row["VisceralFat"] > 10:
        score -= (row["VisceralFat"] - 10) * 2

    if row["BodyWater"] < 50:
        score -= (50 - row["BodyWater"]) * 1.5

    return max(0, round(score))


def ai_coach(row):

    tips = []

    if row["BMI"] > 25:
        tips.append("BMI slightly high. Consider fat reduction.")

    if row["BodyFat"] > 20:
        tips.append("Body fat above optimal. Add cardio training.")

    if row["VisceralFat"] > 10:
        tips.append("Visceral fat elevated. Improve diet.")

    if row["BodyWater"] < 50:
        tips.append("Hydration appears low. Increase water intake.")

    if not tips:
        tips.append("Body composition is within healthy range.")

    return tips


# ------------------------------------------------------------
# Load Dataset
# ------------------------------------------------------------

df = None

if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)

# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.title("📊 FitCom Dashboard")

    if df is None or df.empty:

        st.info("No reports available yet.")

    else:

        st.subheader("All Recorded Reports")

        st.dataframe(df)

        latest = df.iloc[-1]

        st.subheader("Latest Body Metrics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("BMI", latest["BMI"])
        col2.metric("Body Fat %", latest["BodyFat"])
        col3.metric("Muscle Mass", latest["MuscleMass"])
        col4.metric("Visceral Fat", latest["VisceralFat"])

        score = calculate_fitness_score(latest)

        st.subheader("Fitness Score")

        st.progress(score / 100)

        st.metric("Score", f"{score}/100")


# ============================================================
# ADD REPORT
# ============================================================

elif page == "Add Report":

    st.title("➕ Add Body Composition Report")

    name = st.text_input("Name")

    age = st.number_input("Age", 10, 100)

    height = st.number_input("Height (inches)", 48, 90)

    weight = st.number_input("Weight (kg)", 30.0, 200.0)

    bmi_auto = calculate_bmi(weight, height)

    bmi = st.number_input(
        "BMI",
        value=float(bmi_auto) if bmi_auto else 0.0
    )

    bodyfat = st.number_input("Body Fat %", 1.0, 60.0)

    muscle = st.number_input("Muscle Mass", 10.0, 100.0)

    visceral = st.number_input("Visceral Fat", 1.0, 50.0)

    bodywater = st.number_input("Body Water %", 1.0, 80.0)

    if st.button("Save Report"):

        if not name:

            st.error("Name is required")

        else:

            report = {
                "Name": name,
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Age": age,
                "Height": height,
                "Weight": weight,
                "BMI": bmi,
                "BodyFat": bodyfat,
                "MuscleMass": muscle,
                "VisceralFat": visceral,
                "BodyWater": bodywater
            }

            save_report(name, report)

            st.success("Report saved successfully!")


# ============================================================
# PROGRESS
# ============================================================

elif page == "Progress":

    st.title("📈 Progress Tracking")

    if df is None or df.empty:

        st.info("No reports available.")

    else:

        user = st.selectbox("Select User", df["Name"].unique())

        user_df = df[df["Name"] == user].sort_values("Date")

        st.subheader("User Historical Reports")

        st.dataframe(user_df)

        if len(user_df) > 1:

            st.subheader("Progress Chart")

            st.line_chart(
                user_df.set_index("Date")[["Weight", "BodyFat", "MuscleMass"]]
            )

        else:

            st.info("Add multiple reports to see progress.")


# ============================================================
# LEADERBOARD
# ============================================================

elif page == "Leaderboard":

    st.title("🏆 FitCom Leaderboard")

    if df is None or df.empty:

        st.info("No reports available.")

    else:

        df["FitnessScore"] = df.apply(calculate_fitness_score, axis=1)

        leaderboard = df.sort_values("FitnessScore", ascending=False)

        st.dataframe(
            leaderboard[["Name", "Date", "FitnessScore", "BodyFat", "MuscleMass"]],
            use_container_width=True
        )


# ============================================================
# AI COACH
# ============================================================

elif page == "AI Coach":

    st.title("🤖 AI Health Coach")

    if df is None or df.empty:

        st.info("No reports available.")

    else:

        user = st.selectbox("Select User", df["Name"].unique())

        latest = df[df["Name"] == user].iloc[-1]

        st.subheader("Latest Metrics")

        st.write(latest)

        st.subheader("AI Advice")

        tips = ai_coach(latest)

        for tip in tips:
            st.success(tip)