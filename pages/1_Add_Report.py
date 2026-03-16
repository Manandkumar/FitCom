# ============================================================
# Author: Anand Kumar
# ============================================================

import streamlit as st
import uuid
from PIL import Image
import os
from datetime import datetime
from storage import save_report
from sidebar import render_sidebar

# -------------------------------------------------------
# Render Sidebar
# -------------------------------------------------------
render_sidebar()

st.title("➕ Add Body Composition Report")

# -------------------------------------------------------
# Utility Functions
# -------------------------------------------------------

def calculate_bmi(weight, height_in):
    """Calculate BMI using kg and inches"""
    if height_in == 0:
        return 0

    height_m = height_in * 0.0254
    return round(weight / (height_m ** 2), 2)


def calculate_bmr(weight, height_cm, age):
    """Mifflin-St Jeor Equation (male default)"""
    return round((10 * weight) + (6.25 * height_cm) - (5 * age) + 5)


def ideal_body_weight(height_in):
    """Devine formula"""
    return round(50 + 2.3 * (height_in - 60), 1)


def fat_mass(weight, bodyfat):
    return round(weight * bodyfat / 100, 2)


def fat_free_mass(weight, fat_mass):
    return round(weight - fat_mass, 2)


def water_weight(weight, bodywater):
    return round(weight * bodywater / 100, 2)


# -------------------------------------------------------
# Color Status Function
# -------------------------------------------------------

def status_dot(value, green_range, amber_range):
    """
    Returns color emoji for indicator
    """
    if green_range[0] <= value <= green_range[1]:
        return "🟢"
    elif amber_range[0] <= value <= amber_range[1]:
        return "🟡"
    else:
        return "🔴"


# -------------------------------------------------------
# Image Upload Function
# -------------------------------------------------------

def save_image(uploaded_file):

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


# -------------------------------------------------------
# User Profile Section
# -------------------------------------------------------

st.subheader("User Profile")

uploaded_photo = st.file_uploader(
    "Upload Selfie",
    type=["jpg","jpeg","png"]
)

photo_path = None
preview = None

if uploaded_photo:
    photo_path, preview = save_image(uploaded_photo)

    if preview:
        st.image(preview, width=200)

name = st.text_input("Name")

age = st.number_input("Age", min_value=10, max_value=100)

height = st.number_input("Height (inches)", min_value=48, max_value=90)

height_cm = height * 2.54


# -------------------------------------------------------
# Body Metrics Input
# -------------------------------------------------------

st.subheader("Body Composition Metrics")

weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0)

# BMI auto calculated
bmi = calculate_bmi(weight, height)
bmi_status = status_dot(bmi,(18.5,24.9),(25,29.9))
st.metric("BMI", f"{bmi} {bmi_status}")


# -------------------------------------------------------
# Body Fat
# -------------------------------------------------------

bodyfat = st.number_input("Body Fat %", min_value=1.0, max_value=60.0)

bodyfat_status = status_dot(bodyfat,(10,20),(20,25))

st.write(f"Body Fat Status {bodyfat_status}")

fat_mass_value = fat_mass(weight, bodyfat)
st.metric("Fat Mass (kg)", fat_mass_value)

ffbw = fat_free_mass(weight, fat_mass_value)
st.metric("Fat Free Body Weight", ffbw)


# -------------------------------------------------------
# Muscle Metrics
# -------------------------------------------------------

muscle_mass = st.number_input("Muscle Mass (kg)", min_value=10.0, max_value=100.0)

muscle_rate = round((muscle_mass / weight) * 100,2) if weight>0 else 0

st.metric("Muscle Rate %", muscle_rate)

skeletal_muscle = st.number_input("Skeletal Muscle %", min_value=10.0, max_value=60.0)

bone_mass = st.number_input("Bone Mass (kg)", min_value=1.0, max_value=10.0)


# -------------------------------------------------------
# Protein Metrics
# -------------------------------------------------------

protein_mass = st.number_input("Protein Mass (kg)", min_value=1.0, max_value=30.0)

protein_rate = round((protein_mass / weight)*100,2) if weight>0 else 0

st.metric("Protein Rate %", protein_rate)


# -------------------------------------------------------
# Water Metrics
# -------------------------------------------------------

body_water = st.number_input("Body Water %", min_value=1.0, max_value=80.0)

water_weight_value = water_weight(weight, body_water)

st.metric("Water Weight (kg)", water_weight_value)


# -------------------------------------------------------
# Fat Distribution
# -------------------------------------------------------

subcutaneous_fat = st.number_input("Subcutaneous Fat %", min_value=1.0, max_value=50.0)

visceral_fat = st.number_input("Visceral Fat Level", min_value=1.0, max_value=30.0)

visceral_status = status_dot(visceral_fat,(1,10),(11,15))

st.write(f"Visceral Fat Status {visceral_status}")


# -------------------------------------------------------
# Metabolic Metrics
# -------------------------------------------------------

bmr = calculate_bmr(weight,height_cm,age)

st.metric("BMR (Calories/day)",bmr)

body_age = st.number_input("Body Age", min_value=10, max_value=100)

whr = st.number_input("WHR (Waist Hip Ratio)", min_value=0.5, max_value=2.0)

ideal_weight = ideal_body_weight(height)

st.metric("Ideal Body Weight", ideal_weight)


# -------------------------------------------------------
# Save Report
# -------------------------------------------------------

st.divider()

if st.button("Save Report"):

    if name.strip() == "":
        st.error("Name required")

    else:

        report = {

            "Name": name,
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
            "ProteinMass": protein_mass,
            "ProteinRate": protein_rate,
            "WaterWeight": water_weight_value,
            "BodyWater": body_water,
            "SubcutaneousFat": subcutaneous_fat,
            "VisceralFat": visceral_fat,
            "BMR": bmr,
            "BodyAge": body_age,
            "WHR": whr,
            "IdealBodyWeight": ideal_weight
        }

        save_report(name, report)

        st.success("Report saved successfully")
