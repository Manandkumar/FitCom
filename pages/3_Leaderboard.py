import streamlit as st
import pandas as pd
import os
from sidebar import render_sidebar

render_sidebar()

FILE_NAME = "fitcom_reports.csv"

st.title("🏆 FitCom Leaderboard")

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
# Load Data
# ------------------------------------------------------------

if os.path.exists(FILE_NAME):

    df = pd.read_csv(FILE_NAME)

    # ------------------------------------------------------------
    # Most Improved Athlete
    # ------------------------------------------------------------

    st.subheader("🔥 Most Improved Athlete")

    improvements = []

    for athlete in df["Name"].unique():

        athlete_df = df[df["Name"] == athlete].sort_values("Date")

        if len(athlete_df) > 1:

            start_fat = athlete_df.iloc[0]["BodyFat"]
            end_fat = athlete_df.iloc[-1]["BodyFat"]

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
    # Leaderboard (Latest record per user)
    # ------------------------------------------------------------

    st.subheader("🏅 Fitness Leaderboard")

    latest_df = (
        df.sort_values("Date")
        .groupby("Name")
        .tail(1)
    )

    latest_df["FitnessScore"] = latest_df.apply(calculate_fitness_score, axis=1)

    leaderboard = latest_df.sort_values("FitnessScore", ascending=False)

    athletes = leaderboard.to_dict("records")

    cols = st.columns(len(athletes))

    for col, athlete in zip(cols, athletes):

        with col:

            # Photo
            if "Photo" in athlete and pd.notna(athlete["Photo"]):

                if os.path.exists(athlete["Photo"]):

                    st.image(athlete["Photo"], width=120)

            else:
                st.image(
                    "https://cdn-icons-png.flaticon.com/512/149/149071.png",
                    width=120
                )

            # Name
            st.markdown(f"### {athlete['Name']}")

            # Score
            st.metric("🏆 Fitness Score", athlete["FitnessScore"])

            # Metrics
            st.metric("⚖️ BMI", athlete["BMI"])
            st.metric("🔥 Body Fat %", athlete["BodyFat"])
            st.metric("💪 Muscle", athlete["MuscleMass"])

else:

    st.info("No reports available yet.")