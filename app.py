# -------------------------------------------------------
# FitCom - Body Composition Dashboard
# Author: Anand Kumar
# -------------------------------------------------------

import streamlit as st
import pandas as pd
import os
from datetime import datetime

from storage import save_report

FILE_NAME = "fitcom_reports.csv"

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="FitCom",
    layout="wide"
)

st.title("🏋️ FitCom - Body Composition Dashboard")

st.write(
    "Track body composition metrics, monitor progress, and compare performance."
)

# -------------------------------------------------------
# HEALTH STATUS DOT
# -------------------------------------------------------

def status_dot(value, green_range, orange_range):

    if value is None:
        return ""

    if green_range[0] <= value <= green_range[1]:
        return "🟢"

    elif orange_range[0] <= value <= orange_range[1]:
        return "🟠"

    else:
        return "🔴"


# -------------------------------------------------------
# BMI CALCULATION
# -------------------------------------------------------

def calculate_bmi(weight, height_in):

    if height_in == 0:
        return None

    height_m = height_in * 0.0254

    bmi = weight / (height_m ** 2)

    return round(bmi, 2)


# -------------------------------------------------------
# USER ENTRY
# -------------------------------------------------------

st.subheader("👤 Enter Body Metrics")

with st.form("entry_form"):

    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input("Name *")

    with col2:
        age = st.number_input("Age", 10, 100)

    with col3:
        height = st.number_input("Height (inches)", 48, 90)

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        weight = st.number_input("Weight (kg)", 30.0, 200.0)

        bmi_auto = calculate_bmi(weight, height)

        bmi = st.number_input(
            "BMI (auto calculated)",
            value=float(bmi_auto) if bmi_auto else 0.0
        )

        bodyfat = st.number_input("Body Fat (%)", 1.0, 60.0)

        fat_mass = st.number_input("Fat Mass (kg)", 1.0, 100.0)

        fat_free = st.number_input("Fat Free Body Weight (kg)", 10.0, 150.0)

    with col2:

        muscle_mass = st.number_input("Muscle Mass (kg)", 10.0, 100.0)

        muscle_rate = st.number_input("Muscle Rate (%)", 10.0, 90.0)

        skeletal_muscle = st.number_input("Skeletal Muscle (%)", 10.0, 80.0)

        bone_mass = st.number_input("Bone Mass (kg)", 1.0, 10.0)

        protein_mass = st.number_input("Protein Mass (kg)", 1.0, 30.0)

    with col3:

        protein = st.number_input("Protein (%)", 1.0, 40.0)

        water_weight = st.number_input("Water Weight (kg)", 1.0, 100.0)

        body_water = st.number_input("Body Water (%)", 1.0, 80.0)

        visceral_fat = st.number_input("Visceral Fat", 1.0, 50.0)

        bmr = st.number_input("BMR", 800.0, 4000.0)

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        body_age = st.number_input("Body Age", 10, 100)

    with col2:
        whr = st.number_input("WHR", 0.5, 1.5)

    with col3:
        ideal_weight = st.number_input("Ideal Body Weight (kg)", 30.0, 150.0)

    submitted = st.form_submit_button("Save Report")

# -------------------------------------------------------
# SAVE DATA
# -------------------------------------------------------

if submitted:

    if not name:

        st.error("Name is mandatory")

    else:

        report_date = datetime.now().strftime("%Y-%m-%d")

        metrics = {

            "Name": name,
            "Date": report_date,
            "Age": age,
            "Height": height,
            "Weight": weight,
            "BMI": bmi,
            "BodyFat": bodyfat,
            "FatMass": fat_mass,
            "FatFreeWeight": fat_free,
            "MuscleMass": muscle_mass,
            "MuscleRate": muscle_rate,
            "SkeletalMuscle": skeletal_muscle,
            "BoneMass": bone_mass,
            "ProteinMass": protein_mass,
            "Protein": protein,
            "WaterWeight": water_weight,
            "BodyWater": body_water,
            "VisceralFat": visceral_fat,
            "BMR": bmr,
            "BodyAge": body_age,
            "WHR": whr,
            "IdealWeight": ideal_weight
        }

        save_report(name, metrics)

        st.success("Report saved successfully!")


# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

if os.path.exists(FILE_NAME):

    df = pd.read_csv(FILE_NAME)

    st.subheader("📊 All Reports")

    st.dataframe(df)


# -------------------------------------------------------
# USER PROGRESS GRAPH
# -------------------------------------------------------

    st.subheader("📈 Progress Tracking")

    users = df["Name"].unique()

    selected_user = st.selectbox("Select User", users)

    user_df = df[df["Name"] == selected_user]

    if len(user_df) > 1:

        chart_df = user_df.set_index("Date")[["Weight","BodyFat","MuscleMass"]]

        st.line_chart(chart_df)

    else:

        st.info("Add more reports to see progress trend.")


# -------------------------------------------------------
# HEALTH STATUS SUMMARY
# -------------------------------------------------------

    st.subheader("🟢 Health Status")

    latest = user_df.iloc[-1]

    st.write(
        "BMI:",
        latest["BMI"],
        status_dot(latest["BMI"], (18.5,24.9),(25,29.9))
    )

    st.write(
        "Body Fat:",
        latest["BodyFat"],
        status_dot(latest["BodyFat"], (10,20),(21,25))
    )

    st.write(
        "Visceral Fat:",
        latest["VisceralFat"],
        status_dot(latest["VisceralFat"], (1,9),(10,14))
    )

    st.write(
        "Body Water:",
        latest["BodyWater"],
        status_dot(latest["BodyWater"], (50,65),(45,49))
    )

    # -------------------------------------------------------
# GLOBAL COMPARISON ACROSS ALL USERS
# -------------------------------------------------------

st.subheader("⚖️ FitCom Global Comparison")

if len(df) > 1:

    numeric_cols = df.select_dtypes(include=["int64","float64"]).columns

    # remove age and height from comparison
    numeric_cols = [c for c in numeric_cols if c not in ["Age","Height"]]

    comparison_results = []

    for metric in numeric_cols:

        best_idx = df[metric].idxmax()
        worst_idx = df[metric].idxmin()

        best_person = df.loc[best_idx]["Name"]
        worst_person = df.loc[worst_idx]["Name"]

        best_value = df.loc[best_idx][metric]
        worst_value = df.loc[worst_idx][metric]

        comparison_results.append({
            "Metric": metric,
            "Best Performer": best_person,
            "Best Value": best_value,
            "Lowest Performer": worst_person,
            "Lowest Value": worst_value
        })

    comparison_df = pd.DataFrame(comparison_results)

    st.dataframe(comparison_df)

else:

    st.info("Add more participants to enable comparison.")