# ============================================================
# FitCom - Add Body Composition Report
# Author: Anand Kumar
#
# Purpose:
# Capture and store member body composition data
# with real-time calculations and insights.
#
# Design Notes:
# - Structured sections for better UX
# - Real-time metrics for instant feedback
# - Optimized layout using columns (less scrolling)
# ============================================================

import streamlit as st
import uuid
from PIL import Image
import os
from datetime import datetime
from storage import save_report
from sidebar import render_sidebar

# -------------------------------------------------------
# INIT
# -------------------------------------------------------

render_sidebar()

st.markdown("<h2>Add Member Report</h2>", unsafe_allow_html=True)
st.caption("Capture body composition and fitness metrics")

# -------------------------------------------------------
# UTILITY FUNCTIONS
# -------------------------------------------------------

def calculate_bmi(weight, height_in):
    """
    Calculate BMI from weight (kg) and height (inches)
    Handles division-by-zero edge case
    """
    if height_in == 0:
        return 0
    height_m = height_in * 0.0254
    return round(weight / (height_m ** 2), 2)


def calculate_bmr(weight, height_cm, age, gender):
    """
    Mifflin-St Jeor Equation
    Used for estimating daily calorie needs
    """
    if gender == "Male":
        return round((10 * weight) + (6.25 * height_cm) - (5 * age) + 5)
    else:
        return round((10 * weight) + (6.25 * height_cm) - (5 * age) - 161)


def ideal_body_weight(height_in):
    """Devine formula for ideal weight"""
    return round(50 + 2.3 * (height_in - 60), 1)


def fat_mass(weight, bodyfat):
    return round(weight * bodyfat / 100, 2)


def fat_free_mass(weight, fat_mass):
    return round(weight - fat_mass, 2)


def water_weight(weight, bodywater):
    return round(weight * bodywater / 100, 2)


def status_dot(value, green_range, amber_range):
    """
    Returns quick visual indicator for health status
    Helps users interpret values without reading ranges
    """
    if green_range[0] <= value <= green_range[1]:
        return "🟢"
    elif amber_range[0] <= value <= amber_range[1]:
        return "🟡"
    else:
        return "🔴"


def save_image(uploaded_file):
    """
    Stores uploaded image locally
    - Converts to JPEG for consistency
    - Generates unique filename
    """
    try:
        image = Image.open(uploaded_file)

        if image.mode != "RGB":
            image = image.convert("RGB")

        os.makedirs("profiles", exist_ok=True)

        filename = f"{uuid.uuid4()}.jpg"
        path = os.path.join("profiles", filename)

        image.save(path, "JPEG")

        return path, image

    except:
        st.error("Image saving failed")
        return None, None


# =======================================================
# USER PROFILE
# =======================================================

st.markdown("<h3>User Profile</h3>", unsafe_allow_html=True)

col1, col2 = st.columns([1,2])

with col1:
    uploaded_photo = st.file_uploader("Upload Selfie", type=["jpg","jpeg","png"])

    photo_path = None
    if uploaded_photo:
        photo_path, preview = save_image(uploaded_photo)
        if preview:
            st.image(preview, width=150)

with col2:
    name = st.text_input("Name")
    gender = st.selectbox("Gender", ["Male","Female"])
    age = st.number_input("Age", 10, 100)
    height = st.number_input("Height (inches)", 48, 90)

height_cm = height * 2.54

# =======================================================
# BODY METRICS
# =======================================================

st.markdown("<h3>Body Composition</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    weight = st.number_input("Weight (kg)", 30.0, 200.0)
    bmi = calculate_bmi(weight, height)
    bmi_status = status_dot(bmi,(18.5,24.9),(25,29.9))
    st.metric("BMI", f"{bmi} {bmi_status}")

with col2:
    bodyfat = st.number_input("Body Fat %", 1.0, 60.0)

    if gender == "Male":
        bodyfat_status = status_dot(bodyfat,(10,20),(20,25))
    else:
        bodyfat_status = status_dot(bodyfat,(18,28),(28,35))

    st.metric("Body Fat", f"{bodyfat}% {bodyfat_status}")

with col3:
    muscle_mass = st.number_input("Muscle Mass (kg)", 10.0, 100.0)
    muscle_rate = round((muscle_mass / weight) * 100,2) if weight>0 else 0
    st.metric("Muscle %", muscle_rate)

# Derived values
fat_mass_value = fat_mass(weight, bodyfat)
ffbw = fat_free_mass(weight, fat_mass_value)

st.metric("Fat Mass", fat_mass_value)
st.metric("Fat Free Mass", ffbw)

# =======================================================
# ADDITIONAL METRICS
# =======================================================

st.markdown("<h3>Additional Metrics</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    body_water = st.number_input("Body Water %", 1.0, 80.0)
    water_weight_value = water_weight(weight, body_water)
    st.metric("Water Weight", water_weight_value)

with col2:
    visceral_fat = st.number_input("Visceral Fat", 1.0, 30.0)
    visceral_status = status_dot(visceral_fat,(1,10),(11,15))
    st.metric("Visceral Fat", f"{visceral_fat} {visceral_status}")

with col3:
    protein_mass = st.number_input("Protein Mass (kg)", 1.0, 30.0)
    protein_rate = round((protein_mass / weight)*100,2) if weight>0 else 0
    st.metric("Protein %", protein_rate)

# =======================================================
# METABOLIC DATA
# =======================================================

st.markdown("<h3>Metabolic Insights</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    bmr = calculate_bmr(weight,height_cm,age,gender)
    st.metric("BMR", bmr)

with col2:
    ideal_weight = ideal_body_weight(height)
    st.metric("Ideal Weight", ideal_weight)

# =======================================================
# SAVE REPORT
# =======================================================

st.divider()

if st.button("Save Report"):

    if name.strip() == "":
        st.error("Name required")

    else:

        # Persist full report (acts as history log)
        report = {
            "Name": name,
            "Gender": gender,
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Photo": photo_path,
            "Age": age,
            "Height": height,
            "Weight": weight,
            "BMI": bmi,
            "BodyFat": bodyfat,
            "FatMass": fat_mass_value,
            "FatFreeBodyWeight": ffbw,
            "MuscleMass": muscle_mass,
            "MuscleRate": muscle_rate,
            "BodyWater": body_water,
            "WaterWeight": water_weight_value,
            "ProteinMass": protein_mass,
            "ProteinRate": protein_rate,
            "VisceralFat": visceral_fat,
            "BMR": bmr,
            "IdealBodyWeight": ideal_weight
        }

        save_report(name, report)

        st.success("Report saved successfully ✅")