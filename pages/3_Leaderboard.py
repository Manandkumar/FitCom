import streamlit as st
import pandas as pd
import os
import base64
from sidebar import render_sidebar

render_sidebar()

FILE_NAME = "fitcom_reports.csv"

# ------------------------------------------------------------
# Styling
# ------------------------------------------------------------

st.markdown("""
<style>

table {
    font-size:16px !important;
}

thead th {
    text-align:center !important;
    font-size:18px !important;
}

tbody td {
    text-align:center !important;
}

</style>
""", unsafe_allow_html=True)

st.title("🏆 FitCom Leaderboard")

# ------------------------------------------------------------
# Image Encoder
# ------------------------------------------------------------

def get_image_base64(path):

    try:
        with open(path, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        return f"<img src='data:image/png;base64,{encoded}' width='80'>"
    except:
        return "—"

# ------------------------------------------------------------
# Fitness Score Function
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# Health Indicators
# ------------------------------------------------------------

def bmi_indicator(bmi):

    if bmi < 18.5:
        return "🟡"

    elif bmi <= 24.9:
        return "🟢"

    elif bmi <= 29.9:
        return "🟡"

    else:
        return "🔴"


def bodyfat_indicator(bodyfat):

    if bodyfat <= 15:
        return "🟢"

    elif bodyfat <= 20:
        return "🟢"

    elif bodyfat <= 25:
        return "🟡"

    else:
        return "🔴"


def visceral_indicator(visceral):

    if visceral <= 9:
        return "🟢"

    elif visceral <= 14:
        return "🟡"

    else:
        return "🔴"


# ------------------------------------------------------------
# Load Data
# ------------------------------------------------------------

if os.path.exists(FILE_NAME):

    df = pd.read_csv(FILE_NAME)

    # ------------------------------------------------------------
    # Latest record per athlete
    # ------------------------------------------------------------

    latest_df = (
        df.sort_values("Date")
        .groupby("Name")
        .tail(1)
    )

    latest_df["FitnessScore"] = latest_df.apply(calculate_fitness_score, axis=1)

    leaderboard = latest_df.sort_values("FitnessScore", ascending=False)

    athletes = leaderboard["Name"].tolist()

    rows = []

    # ------------------------------------------------------------
    # PHOTO ROW
    # ------------------------------------------------------------

    photo_row = {"Metric": "Photo"}

    for _, row in leaderboard.iterrows():

        photo_path = row.get("Photo", "")

        if pd.notna(photo_path) and os.path.exists(photo_path):
            photo_html = get_image_base64(photo_path)
        else:
            photo_html = "—"

        photo_row[row["Name"]] = photo_html

    rows.append(photo_row)

    # ------------------------------------------------------------
    # RANK ROW
    # ------------------------------------------------------------

    rank_row = {"Metric": "Rank"}

    for i, (_, row) in enumerate(leaderboard.iterrows()):

        if i == 0:
            medal = "🥇"
        elif i == 1:
            medal = "🥈"
        elif i == 2:
            medal = "🥉"
        else:
            medal = str(i+1)

        rank_row[row["Name"]] = medal

    rows.append(rank_row)

    # ------------------------------------------------------------
    # FITNESS SCORE
    # ------------------------------------------------------------

    score_row = {"Metric": "Fitness Score"}

    for _, row in leaderboard.iterrows():
        score_row[row["Name"]] = row["FitnessScore"]

    rows.append(score_row)

    # ------------------------------------------------------------
    # WEIGHT
    # ------------------------------------------------------------

    weight_row = {"Metric": "Weight"}

    for _, row in leaderboard.iterrows():
        weight_row[row["Name"]] = row.get("Weight","NA")

    rows.append(weight_row)

    # ------------------------------------------------------------
    # BMI
    # ------------------------------------------------------------

    bmi_row = {"Metric": "BMI"}

    for _, row in leaderboard.iterrows():

        bmi = row.get("BMI","NA")

        bmi_row[row["Name"]] = f"{bmi} {bmi_indicator(bmi)}"

    rows.append(bmi_row)

    # ------------------------------------------------------------
    # BODY FAT
    # ------------------------------------------------------------

    fat_row = {"Metric": "Body Fat"}

    for _, row in leaderboard.iterrows():

        bf = row.get("BodyFat","NA")

        fat_row[row["Name"]] = f"{bf} {bodyfat_indicator(bf)}"

    rows.append(fat_row)

    # ------------------------------------------------------------
    # MUSCLE MASS
    # ------------------------------------------------------------

    muscle_row = {"Metric": "Muscle Mass"}

    for _, row in leaderboard.iterrows():
        muscle_row[row["Name"]] = row.get("MuscleMass","NA")

    rows.append(muscle_row)

    # ------------------------------------------------------------
    # BODY WATER
    # ------------------------------------------------------------

    water_row = {"Metric": "Body Water"}

    for _, row in leaderboard.iterrows():
        water_row[row["Name"]] = row.get("BodyWater","NA")

    rows.append(water_row)

    # ------------------------------------------------------------
    # VISCERAL FAT
    # ------------------------------------------------------------

    vis_row = {"Metric": "Visceral Fat"}

    for _, row in leaderboard.iterrows():

        vf = row.get("VisceralFat","NA")

        vis_row[row["Name"]] = f"{vf} {visceral_indicator(vf)}"

    rows.append(vis_row)

    # ------------------------------------------------------------
    # BMR
    # ------------------------------------------------------------

    bmr_row = {"Metric": "BMR"}

    for _, row in leaderboard.iterrows():
        bmr_row[row["Name"]] = row.get("BMR","NA")

    rows.append(bmr_row)

    # ------------------------------------------------------------
    # Build Table
    # ------------------------------------------------------------

    table_df = pd.DataFrame(rows)

    st.subheader("🏅 Fitness Comparison")

    st.write(
        table_df.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )

else:

    st.info("No reports available yet.")