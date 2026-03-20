# ============================================================
# FitCom - Leaderboard (DB VERSION - STABLE)
# ============================================================

import streamlit as st
import pandas as pd
import base64
import os

from storage import load_reports
from sidebar import render_sidebar
from ui.theme import apply_theme
from ui.components import page_header, section, card

# -------------------------------------------------------
# INIT
# -------------------------------------------------------

render_sidebar()
apply_theme()

page_header("Leaderboard", "Top performers based on fitness score")

# -------------------------------------------------------
# STYLING (UNCHANGED)
# -------------------------------------------------------

st.markdown("""
<style>
table {
    border-collapse: separate !important;
    border-spacing: 0 10px;
    font-size: 14px !important;
}
thead th {
    text-align: center !important;
    background: #f4f6f8;
    padding: 10px !important;
    border: none !important;
}
tbody tr {
    background: white;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
}
tbody td {
    padding: 10px !important;
    border: none !important;
    text-align: center;
}
tbody tr td:first-child {
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
}
tbody tr td:last-child {
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
}
img {
    width: 50px !important;
    height: 50px !important;
    object-fit: cover;
    border-radius: 8px;
}
.indicator {
    display: inline-flex;
    align-items: center;
    gap: 4px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# UTILITIES
# -------------------------------------------------------

def get_image_base64(path):
    try:
        with open(path, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        return f"<img src='data:image/png;base64,{encoded}'>"
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

# Convert Date safely
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Drop invalid dates
df = df.dropna(subset=["Date"])

# -------------------------------------------------------
# GET LATEST RECORD PER USER
# -------------------------------------------------------

latest_df = df.sort_values("Date").groupby("Name").tail(1)

# Calculate score
latest_df["FitnessScore"] = latest_df.apply(calculate_fitness_score, axis=1)

leaderboard = latest_df.sort_values("FitnessScore", ascending=False)

# -------------------------------------------------------
# TOP 3 SECTION
# -------------------------------------------------------

section("Top Performers")

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
# FULL LEADERBOARD
# -------------------------------------------------------

section("Full Leaderboard")

rows = []

for i, (_, row) in enumerate(leaderboard.iterrows()):

    # Rank logic
    if i == 0:
        rank = "🥇"
    elif i == 1:
        rank = "🥈"
    elif i == 2:
        rank = "🥉"
    else:
        rank = str(i + 1)

    # Photo handling
    photo = row.get("Photo", "")
    if pd.notna(photo) and isinstance(photo, str) and os.path.exists(photo):
        photo_html = get_image_base64(photo)
    else:
        photo_html = "—"

    rows.append({
        "Rank": rank,
        "Photo": photo_html,
        "Name": row["Name"],
        "Fitness Score": row["FitnessScore"],
        "Weight": row.get("Weight", "NA"),
        "BMI": f"<span class='indicator'>{row.get('BMI','NA')} {indicator(row.get('BMI',0),24.9,29.9)}</span>",
        "Body Fat": f"<span class='indicator'>{row.get('BodyFat','NA')} {indicator(row.get('BodyFat',0),20,25)}</span>",
        "Muscle Mass": row.get("MuscleMass", "NA"),
        "Body Water": row.get("BodyWater", "NA"),
        "Visceral Fat": f"<span class='indicator'>{row.get('VisceralFat','NA')} {indicator(row.get('VisceralFat',0),10,15)}</span>",
        "BMR": row.get("BMR", "NA")
    })

table_df = pd.DataFrame(rows)

card(table_df.to_html(escape=False, index=False))