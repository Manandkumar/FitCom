# ============================================================
# FitCom - Leaderboard (Using UI Layer)
# ============================================================

import streamlit as st
import pandas as pd
import os
import base64

from sidebar import render_sidebar
from ui.theme import apply_theme
from ui.components import page_header, section, card

# -------------------------------------------------------
# INIT
# -------------------------------------------------------

render_sidebar()
apply_theme()

FILE_NAME = "fitcom_reports.csv"

page_header("Leaderboard", "Top performers based on fitness score")

# -------------------------------------------------------
# UTILITIES
# -------------------------------------------------------

def get_image_base64(path):
    try:
        with open(path, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        return f"<img src='data:image/png;base64,{encoded}' width='60'>"
    except:
        return "—"


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


def indicator(value, good, mid):
    if value <= good:
        return "🟢"
    elif value <= mid:
        return "🟡"
    return "🔴"

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

if os.path.exists(FILE_NAME):

    df = pd.read_csv(FILE_NAME)

    # Always use latest record per user
    latest_df = df.sort_values("Date").groupby("Name").tail(1)

    latest_df["FitnessScore"] = latest_df.apply(calculate_fitness_score, axis=1)

    leaderboard = latest_df.sort_values("FitnessScore", ascending=False)

    # -------------------------------------------------------
    # TOP 3 (CARD)
    # -------------------------------------------------------

    top3 = leaderboard.head(3)

    cols = st.columns(3)
    medals = ["🥇", "🥈", "🥉"]

    for i, (_, row) in enumerate(top3.iterrows()):
        with cols[i]:
            st.metric(
                f"{medals[i]} {row['Name']}",
                f"{row['FitnessScore']}/100"
            )

    # -------------------------------------------------------
    # FULL TABLE (CARD)
    # -------------------------------------------------------

    section("Full Leaderboard")

    rows = []

    for i, (_, row) in enumerate(leaderboard.iterrows()):

        rank = ["🥇","🥈","🥉"][i] if i < 3 else str(i+1)

        photo = row.get("Photo", "")
        if pd.notna(photo) and os.path.exists(photo):
            photo_html = get_image_base64(photo)
        else:
            photo_html = "—"

        rows.append({
            "Rank": rank,
            "Photo": photo_html,
            "Name": row["Name"],
            "Score": row["FitnessScore"],
            "BMI": f"{row.get('BMI','-')} {indicator(row.get('BMI',0),24.9,29.9)}",
            "Body Fat": f"{row.get('BodyFat','-')} {indicator(row.get('BodyFat',0),20,25)}",
            "Muscle": row.get("MuscleMass","-"),
            "Water": row.get("BodyWater","-"),
            "Visceral": f"{row.get('VisceralFat','-')} {indicator(row.get('VisceralFat',0),10,15)}"
        })

    table_df = pd.DataFrame(rows)

    # Wrap table inside card
    card(table_df.to_html(escape=False, index=False))

else:
    st.info("No reports available yet.")