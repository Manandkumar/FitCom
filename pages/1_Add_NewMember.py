# ============================================================
# FitCom - Add Body Composition Report (Premium UI)
# Author: Anand Kumar
#
# Purpose:
# Capture member fitness data with structured UI + real-time insights
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

# -------------------------------------------------------
# GLOBAL UI FIX (Compact + Professional Look)
# -------------------------------------------------------

st.markdown("""
<style>

/* Compact inputs */
input, select {
    height: 36px !important;
    padding: 6px !important;
}

/* Number input */
div[data-baseweb="input"] {
    height: 36px !important;
}

/* Labels */
label {
    font-size: 13px !important;
    margin-bottom: 2px !important;
}

/* Reduce spacing */
.stNumberInput, .stTextInput, .stSelectbox {
    margin-bottom: 8px !important;
}

/* Metrics */
div[data-testid="metric-container"] {
    padding: 6px !important;
}

/* Container spacing */
.block-container {
    padding-top: 1rem;
}

/* CARD STYLE */
.card {
    background: white;
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
    margin-bottom: 14px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

st.markdown("<h2>Add Member Report</h2>", unsafe_allow_html=True)
st.caption("Capture body composition and fitness metrics")

# -------------------------------------------------------
# UTILITIES
# -------------------------------------------------------

def calculate_bmi(weight, height_in):
    if height_in == 0:
        return 0
    return round(weight / ((height_in * 0.0254) ** 2), 2)


def calculate_bmr(weight, height_cm, age, gender):
    if gender == "Male":
        return round((10 * weight) + (6.25 * height_cm) - (5 * age) + 5)
    return round((10 * weight) + (6.25 * height_cm) - (5 * age) - 161)


def ideal_body_weight(height_in):
    return round(50 + 2.3 * (height_in - 60), 1)


def fat_mass(weight, bodyfat):
    return round(weight * bodyfat / 100, 2)


def fat_free_mass(weight, fat_mass):
    return round(weight - fat_mass, 2)


def water_weight(weight, bodywater):
    return round(weight * bodywater / 100, 2)


def save_image(uploaded_file):
    try:
        image = Image.open(uploaded_file)

        if image.mode != "RGB":
            image = image.convert("RGB")

        os.makedirs("profiles", exist_ok=True)

        path = os.path.join("profiles", f"{uuid.uuid4()}.jpg")
        image.save(path, "JPEG")

        return path, image

    except:
        st.error("Image saving failed")
        return None, None


# =======================================================
# USER PROFILE (CARD)
# =======================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)

st.markdown("<h3>User Profile</h3>", unsafe_allow_html=True)

col1, col2 = st.columns([1,2])

with col1:
    uploaded_photo = st.file_uploader("Upload Selfie", type=["jpg","jpeg","png"])
    photo_path = None

    if uploaded_photo:
        photo_path, preview = save_image(uploaded_photo)
        if preview:
            st.image(preview, width=120)

with col2:
    name = st.text_input("Name")
    gender = st.selectbox("Gender", ["Male","Female"])

    c1, c2 = st.columns(2)
    age = c1.number_input("Age", 10, 100)
    height = c2.number_input("Height (inches)", 48, 90)

st.markdown("</div>", unsafe_allow_html=True)

height_cm = height * 2.54

# =======================================================
# BODY COMPOSITION (CARD)
# =======================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)

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

c1, c2 = st.columns(2)
c1.metric("Fat Mass", fat_mass_value)
c2.metric("Fat Free Mass", ffbw)

st.markdown("</div>", unsafe_allow_html=True)

# =======================================================
# ADVANCED METRICS (CARD)
# =======================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)

st.markdown("<h3>Advanced Metrics</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

skeletal_muscle = col1.number_input("Skeletal Muscle %", 10.0, 60.0)
bone_mass = col2.number_input("Bone Mass (kg)", 1.0, 10.0)
subcutaneous_fat = col3.number_input("Subcutaneous Fat %", 1.0, 50.0)

st.markdown("</div>", unsafe_allow_html=True)

# =======================================================
# HYDRATION & PROTEIN (CARD)
# =======================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)

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

st.markdown("</div>", unsafe_allow_html=True)

# =======================================================
# METABOLIC (CARD)
# =======================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)

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

st.markdown("</div>", unsafe_allow_html=True)

# =======================================================
# SAVE BUTTON
# =======================================================

st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)

if st.button("Save Report", use_container_width=True):

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

st.markdown("</div>", unsafe_allow_html=True)