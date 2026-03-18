# ============================================================
# FitCom - Add Body Composition Report
# Author: Anand Kumar
#
# Purpose:
# Capture member body composition data with real-time insights
# and store it for progress tracking and analytics.
#
# Notes:
# - UI optimized for readability (uniform fonts, compact layout)
# - All original fields retained (no data loss)
# - Designed for daily use in gym / fitness environment
# ============================================================

import streamlit as st
import uuid
from PIL import Image
import os
from datetime import datetime
from storage import save_report
from sidebar import render_sidebar

# -------------------------------------------------------
# INITIALIZE PAGE
# -------------------------------------------------------

render_sidebar()

# -------------------------------------------------------
# GLOBAL UI FIX (Uniform font + compact layout)
# -------------------------------------------------------

st.markdown("""
<style>

/* Global font consistency */
html, body, [class*="css"] {
    font-size: 14px !important;
}

/* Labels */
label {
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* Inputs */
input, select {
    font-size: 14px !important;
}

/* Metrics */
div[data-testid="metric-container"] {
    padding: 8px !important;
}

div[data-testid="metric-container"] label {
    font-size: 12px !important;
}

div[data-testid="metric-container"] div {
    font-size: 16px !important;
    font-weight: 600;
}

/* Reduce spacing */
.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# PAGE HEADER
# -------------------------------------------------------

st.markdown("<h2>Add Member Report</h2>", unsafe_allow_html=True)
st.caption("Capture body composition and fitness metrics")

# -------------------------------------------------------
# UTILITY FUNCTIONS
# -------------------------------------------------------

def calculate_bmi(weight, height_in):
    """BMI using kg + inches (handles zero height safely)"""
    if height_in == 0:
        return 0
    height_m = height_in * 0.0254
    return round(weight / (height_m ** 2), 2)


def calculate_bmr(weight, height_cm, age, gender):
    """Mifflin-St Jeor Equation for calorie estimation"""
    if gender == "Male":
        return round((10 * weight) + (6.25 * height_cm) - (5 * age) + 5)
    else:
        return round((10 * weight) + (6.25 * height_cm) - (5 * age) - 161)


def ideal_body_weight(height_in):
    """Devine formula"""
    return round(50 + 2.3 * (height_in - 60), 1)


def fat_mass(weight, bodyfat):
    return round(weight * bodyfat / 100, 2)


def fat_free_mass(weight, fat_mass):
    return round(weight - fat_mass, 2)


def water_weight(weight, bodywater):
    return round(weight * bodywater / 100, 2)


def save_image(uploaded_file):
    """Save uploaded image locally with unique name"""
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
            st.image(preview, width=140)

with col2:
    name = st.text_input("Name")
    gender = st.selectbox("Gender", ["Male","Female"])
    age = st.number_input("Age", 10, 100)
    height = st.number_input("Height (inches)", 48, 90)

height_cm = height * 2.54

# =======================================================
# BODY COMPOSITION
# =======================================================

st.markdown("<h3>Body Composition</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    weight = st.number_input("Weight (kg)", 30.0, 200.0)
    bmi = calculate_bmi(weight, height)
    st.metric("BMI", bmi)

with col2:
    bodyfat = st.number_input("Body Fat %", 1.0, 60.0)

with col3:
    muscle_mass = st.number_input("Muscle Mass (kg)", 10.0, 100.0)
    muscle_rate = round((muscle_mass / weight) * 100,2) if weight>0 else 0
    st.metric("Muscle %", muscle_rate)

# Derived
fat_mass_value = fat_mass(weight, bodyfat)
ffbw = fat_free_mass(weight, fat_mass_value)

col1, col2 = st.columns(2)
col1.metric("Fat Mass", fat_mass_value)
col2.metric("Fat Free Mass", ffbw)

# =======================================================
# ADVANCED BODY METRICS
# =======================================================

st.markdown("<h3>Advanced Metrics</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    skeletal_muscle = st.number_input("Skeletal Muscle %", 10.0, 60.0)

with col2:
    bone_mass = st.number_input("Bone Mass (kg)", 1.0, 10.0)

with col3:
    subcutaneous_fat = st.number_input("Subcutaneous Fat %", 1.0, 50.0)

# =======================================================
# HYDRATION & PROTEIN
# =======================================================

st.markdown("<h3>Hydration & Protein</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    body_water = st.number_input("Body Water %", 1.0, 80.0)
    water_weight_value = water_weight(weight, body_water)
    st.metric("Water Weight", water_weight_value)

with col2:
    protein_mass = st.number_input("Protein Mass (kg)", 1.0, 30.0)
    protein_rate = round((protein_mass / weight)*100,2) if weight>0 else 0
    st.metric("Protein %", protein_rate)

with col3:
    visceral_fat = st.number_input("Visceral Fat", 1.0, 30.0)

# =======================================================
# METABOLIC
# =======================================================

st.markdown("<h3>Metabolic Insights</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    bmr = calculate_bmr(weight,height_cm,age,gender)
    st.metric("BMR", bmr)

with col2:
    body_age = st.number_input("Body Age", 10, 100)

with col3:
    whr = st.number_input("WHR", 0.5, 2.0)

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
            "SkeletalMuscle": skeletal_muscle,
            "BoneMass": bone_mass,
            "SubcutaneousFat": subcutaneous_fat,
            "BodyWater": body_water,
            "WaterWeight": water_weight_value,
            "ProteinMass": protein_mass,
            "ProteinRate": protein_rate,
            "VisceralFat": visceral_fat,
            "BMR": bmr,
            "BodyAge": body_age,
            "WHR": whr,
            "IdealBodyWeight": ideal_weight
        }

        save_report(name, report)

        st.success("Report saved successfully ✅")