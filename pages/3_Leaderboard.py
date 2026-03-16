import streamlit as st
import pandas as pd
import os

FILE_NAME = "fitcom_reports.csv"

st.title("🏆 Leaderboard")

def calculate_fitness_score(row):

    score = 100

    if row["BMI"] > 25:
        score -= (row["BMI"] - 25) * 2

    if row["BodyFat"] > 20:
        score -= (row["BodyFat"] - 20) * 1.5

    return max(0, round(score))

if os.path.exists(FILE_NAME):

    df = pd.read_csv(FILE_NAME)

    df["FitnessScore"] = df.apply(calculate_fitness_score, axis=1)

    leaderboard = df.sort_values("FitnessScore", ascending=False)

    st.dataframe(leaderboard)