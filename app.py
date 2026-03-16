# -------------------------------------------------------
# FitCom - AI Fitness Report Analyzer
# Author: Anand Kumar
# -------------------------------------------------------

import streamlit as st
from PIL import Image
import pandas as pd
import os
import pytesseract
import re

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# FitCom modules
from ocr_engine import extract_text
from parser import extract_all_metrics
from storage import save_report
from comparison_engine import compare_reports
from analysis import analyze
from ai_coach import generate_insights


# -------------------------------------------------------
# Helper Function
# -------------------------------------------------------

def extract_number(value):
    numbers = re.findall(r"\d+\.\d+|\d+", str(value))
    if numbers:
        return float(numbers[0])
    return None


# -------------------------------------------------------
# PAGE HEADER
# -------------------------------------------------------

st.title("🏋️ FitCom - AI Fitness Report Analyzer")

st.write(
    "Upload your body composition report and let **FitCom** analyze and compare fitness metrics."
)


# -------------------------------------------------------
# USER INPUT
# -------------------------------------------------------

st.subheader("👤 User Details")

user_name = st.text_input("Enter Your Name")


# -------------------------------------------------------
# FILE UPLOAD
# -------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Body Report Image",
    type=["jpg", "png", "jpeg"]
)


# -------------------------------------------------------
# PROCESS REPORT
# -------------------------------------------------------

if uploaded_file and user_name:

    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Report", width="stretch")

    # OCR Extraction
    text = extract_text(image)

    st.subheader("📄 Extracted Text")

    st.write(text)

    # -------------------------------------------------------
    # EXTRACT ALL METRICS
    # -------------------------------------------------------

    metrics = extract_all_metrics(text)

    st.subheader("📊 Detected Metrics")

    st.json(metrics)

    # -------------------------------------------------------
    # SIMPLE AI INSIGHT
    # -------------------------------------------------------

    if metrics.get("BodyFat"):

        st.subheader("🤖 FitCom AI Insight")

        st.write(analyze(metrics["BodyFat"]))

    # -------------------------------------------------------
    # SAVE REPORT
    # -------------------------------------------------------

    save_report(user_name, metrics)

    st.success("✅ Report saved successfully!")


# -------------------------------------------------------
# LOAD SAVED REPORTS
# -------------------------------------------------------

if os.path.exists("fitcom_reports.csv"):

    df = pd.read_csv("fitcom_reports.csv")

    st.subheader("📊 All Participant Reports")

    st.dataframe(df)

    # -------------------------------------------------------
    # CLEAN NUMERIC COLUMNS
    # -------------------------------------------------------

    df_numeric = df.copy()

    for col in df_numeric.columns:
        if col != "Name":
            df_numeric[col] = df_numeric[col].apply(extract_number)

    # -------------------------------------------------------
    # FITNESS LEADERBOARD
    # -------------------------------------------------------

    if "BodyFat" in df_numeric.columns:

        df_clean = df_numeric.dropna(subset=["BodyFat"])

        df_clean["Score"] = 100 - df_clean["BodyFat"]

        leaderboard = df_clean.sort_values("Score", ascending=False)

        st.subheader("🏆 FitCom Leaderboard")

        st.table(leaderboard[["Name", "BodyFat", "Score"]])

    # -------------------------------------------------------
    # FITNESS CHART
    # -------------------------------------------------------

    if "BodyFat" in df_numeric.columns and "Weight" in df_numeric.columns:

        st.subheader("📈 Fitness Comparison")

        chart_df = df_numeric.set_index("Name")[["BodyFat", "Weight"]]

        st.bar_chart(chart_df)

    # -------------------------------------------------------
    # PARTICIPANT COMPARISON
    # -------------------------------------------------------

    st.subheader("⚖️ FitCom Participant Comparison")

    comparison = compare_reports(df)

    for metric, data in comparison.items():

        st.write(f"**Metric: {metric}**")

        st.write(
            "🏆 Best:",
            data["best_person"],
            "(",
            data["best_value"],
            ")"
        )

        st.write(
            "⚠️ Lowest:",
            data["worst_person"],
            "(",
            data["worst_value"],
            ")"
        )

        st.write("---")

    # -------------------------------------------------------
    # FITCOM AI HEALTH COACH
    # -------------------------------------------------------

    st.subheader("🧠 FitCom AI Health Coach")

    insights = generate_insights(df_numeric)

    for insight in insights:
        st.write("•", insight)