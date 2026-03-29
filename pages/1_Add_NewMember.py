# ============================================================
# FitCom - Add Body Composition Report (SUPABASE STORAGE)
# ============================================================

import streamlit as st
from datetime import datetime

from storage import save_report
from sidebar import render_sidebar
from ui.theme import apply_theme
from ui.components import page_header, section, card_start, card_end

# ✅ NEW IMPORT
from storage.supabase_storage import upload_image

# -------------------------------------------------------
# INIT
# -------------------------------------------------------

render_sidebar()
apply_theme()

page_header("Add Member", "Capture complete body composition data")

# -------------------------------------------------------
# UTIL FUNCTIONS
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


# =======================================================
# USER PROFILE
# =======================================================

section("User Profile")
card_start()

col1, col2 = st.columns([1, 2])

with col1:

    uploaded = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])
    image_url = None

    if uploaded:
        image_url = upload_image(uploaded)

        if image_url:
            st.image(image_url, width=120)
        else:
            st.error("Image upload failed")

with col2:
    name = st.text_input("Name")
    gender = st.selectbox("Gender", ["Male", "Female"])

    c1, c2 = st.columns(2)
    age = c1.number_input("Age", 10, 100)
    height = c2.number_input("Height (inches)", 48, 90)

card_end()

height_cm = height * 2.54

# =======================================================
# BODY COMPOSITION
# =======================================================

section("Body Composition")
card_start()

col1, col2, col3 = st.columns(3)

with col1:
    weight = st.number_input("Weight (kg)", 30.0, 200.0)
    bmi = calculate_bmi(weight, height)
    st.metric("BMI", bmi)

with col2:
    bodyfat = st.number_input("Body Fat %", 1.0, 60.0)

with col3:
    muscle_mass = st.number_input("Muscle Mass (kg)", 10.0, 100.0)
    muscle_rate = round((muscle_mass / weight) * 100, 2) if weight else 0
    st.metric("Muscle %", muscle_rate)

fat_mass_val = fat_mass(weight, bodyfat)
ffm = fat_free_mass(weight, fat_mass_val)

c1, c2 = st.columns(2)
c1.metric("Fat Mass", fat_mass_val)
c2.metric("Fat Free Mass", ffm)

card_end()

# =======================================================
# ADVANCED METRICS
# =======================================================

section("Advanced Metrics")
card_start()

col1, col2, col3 = st.columns(3)

skeletal_muscle = col1.number_input("Skeletal Muscle %", 10.0, 60.0)
bone_mass = col2.number_input("Bone Mass (kg)", 1.0, 10.0)
subcutaneous_fat = col3.number_input("Subcutaneous Fat %", 1.0, 50.0)

card_end()

# =======================================================
# HYDRATION & PROTEIN
# =======================================================

section("Hydration & Protein")
card_start()

col1, col2, col3 = st.columns(3)

with col1:
    body_water = st.number_input("Body Water %", 1.0, 80.0)
    water_weight_val = water_weight(weight, body_water)
    st.metric("Water Weight", water_weight_val)

with col2:
    protein_mass = st.number_input("Protein Mass (kg)", 1.0, 30.0)
    protein_rate = round((protein_mass / weight) * 100, 2) if weight else 0
    st.metric("Protein %", protein_rate)

with col3:
    visceral_fat = st.number_input("Visceral Fat", 1.0, 30.0)

card_end()

# =======================================================
# METABOLIC
# =======================================================

section("Metabolic Insights")
card_start()

col1, col2, col3 = st.columns(3)

with col1:
    bmr = calculate_bmr(weight, height_cm, age, gender)
    st.metric("BMR", bmr)

with col2:
    body_age = st.number_input("Body Age", 10, 100)

with col3:
    whr = st.number_input("WHR", 0.5, 2.0)

ideal_weight = ideal_body_weight(height)
st.metric("Ideal Weight", ideal_weight)

card_end()

# =======================================================
# SAVE
# =======================================================

if st.button("Save Report", use_container_width=True):

    if not name:
        st.error("Name required")

    elif not image_url:
        st.error("Please upload photo")

    else:
        try:
            report = {
                "UserId": st.session_state["user"],   # ✅ IMPORTANT
                "Name": name,
                "Gender": gender,
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Photo": image_url,
                "Age": int(age),
                "Height": float(height),
                "Weight": float(weight),
                "BMI": float(bmi),
                "BodyFat": float(bodyfat),
                "FatMass": float(fat_mass_val),
                "FatFreeBodyWeight": float(ffm),
                "MuscleMass": float(muscle_mass),
                "MuscleRate": float(muscle_rate),
                "SkeletalMuscle": float(skeletal_muscle),
                "BoneMass": float(bone_mass),
                "SubcutaneousFat": float(subcutaneous_fat),
                "BodyWater": float(body_water),
                "WaterWeight": float(water_weight_val),
                "ProteinMass": float(protein_mass),
                "ProteinRate": float(protein_rate),
                "VisceralFat": float(visceral_fat),
                "BMR": float(bmr),
                "BodyAge": int(body_age),
                "WHR": float(whr),
                "IdealBodyWeight": float(ideal_weight)
            }

            save_report(name, report)

            st.success("Report saved successfully ✅")

        except Exception as e:
            st.error(f"Error saving report: {e}")