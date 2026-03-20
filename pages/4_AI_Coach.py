# ============================================================
# FitCom - AI Coach (DB VERSION - STABLE)
# ============================================================

import streamlit as st
import pandas as pd

from storage import load_reports
from sidebar import render_sidebar
from ui.theme import apply_theme
from ui.components import page_header, section, card_start, card_end

# -------------------------------------------------------
# INIT
# -------------------------------------------------------

render_sidebar()
apply_theme()

page_header("AI Coach", "Personalized fitness insights")

# -------------------------------------------------------
# LOAD DATA (DB)
# -------------------------------------------------------

data = load_reports()

if not data:
    st.info("No reports available yet.")
    st.stop()

# Flatten DB data
df = pd.DataFrame(
    [item for sublist in data.values() for item in sublist]
)

# Ensure date format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Drop invalid dates
df = df.dropna(subset=["Date"])

# -------------------------------------------------------
# USER SELECTION
# -------------------------------------------------------

section("Select Member")

card_start()

users = sorted(df["Name"].dropna().unique())

selected_user = st.selectbox("Choose Member", users)

card_end()

# -------------------------------------------------------
# GET LATEST RECORD
# -------------------------------------------------------

user_df = df[df["Name"] == selected_user].sort_values("Date")

if user_df.empty:
    st.warning("No data found for this member.")
    st.stop()

latest = user_df.iloc[-1]

# -------------------------------------------------------
# SHOW LATEST METRICS
# -------------------------------------------------------

section("Latest Metrics")

card_start()

display_df = pd.DataFrame([latest]).drop(columns=["Photo"], errors="ignore")

st.dataframe(display_df, use_container_width=True)

card_end()

# -------------------------------------------------------
# AI COACH LOGIC (SAFE VERSION)
# -------------------------------------------------------

def ai_coach(row):

    tips = []

    bmi = row.get("BMI", 0)
    bodyfat = row.get("BodyFat", 0)
    muscle = row.get("MuscleMass", 0)
    water = row.get("BodyWater", 0)
    visceral = row.get("VisceralFat", 0)
    protein = row.get("ProteinRate", 0)

    # BMI check
    if bmi > 25:
        tips.append("BMI is high. Focus on fat loss and calorie deficit.")

    # Body fat
    if bodyfat > 20:
        tips.append("Body fat is above optimal. Add cardio and monitor diet.")

    # Muscle mass
    if muscle < 30:
        tips.append("Muscle mass is low. Include strength training.")

    # Hydration
    if water < 50:
        tips.append("Hydration is low. Increase water intake.")

    # Visceral fat
    if visceral > 10:
        tips.append("Visceral fat is high. Reduce sugar and processed food.")

    # Protein
    if protein < 15:
        tips.append("Protein intake is low. Increase protein consumption.")

    return tips


tips = ai_coach(latest)

# -------------------------------------------------------
# RECOMMENDATIONS
# -------------------------------------------------------

section("AI Recommendations")

card_start()

if tips:
    for tip in tips:
        st.success(tip)
else:
    st.success("Great job! All parameters are within healthy range 💪")

card_end()

# -------------------------------------------------------
# QUICK INSIGHT
# -------------------------------------------------------

section("Quick Insight")

card_start()

if len(user_df) > 1:
    prev = user_df.iloc[-2]

    weight_change = latest.get("Weight", 0) - prev.get("Weight", 0)
    fat_change = latest.get("BodyFat", 0) - prev.get("BodyFat", 0)

    st.write(f"Weight Change: **{round(weight_change,2)} kg**")
    st.write(f"Body Fat Change: **{round(fat_change,2)} %**")

    if weight_change < 0:
        st.success("Positive trend in weight reduction 📉")
    elif weight_change > 0:
        st.warning("Weight increased. Review diet ⚠️")
    else:
        st.info("Weight stable")

else:
    st.info("Not enough data for trend insights")

card_end()