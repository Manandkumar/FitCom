import streamlit as st
import pandas as pd
import uuid
from PIL import Image
import os
from datetime import datetime
from storage import save_report

FILE_NAME = "fitcom_reports.csv"

st.title("➕ Add Body Composition Report")

# ------------------------------------------------------------
# Utility Function
# ------------------------------------------------------------

def calculate_bmi(weight, height_in):

    if height_in == 0:
        return 0

    height_m = height_in * 0.0254
    return round(weight / (height_m ** 2), 2)

# ------------------------------------------------------------
# Selfie Upload
# ------------------------------------------------------------

st.subheader("User Profile")

selfie = st.file_uploader(
    "Upload Selfie",
    type=["jpg","png","jpeg"]
)

image = None

if selfie:
    image = Image.open(selfie)
    st.image(image, width=200)

# ------------------------------------------------------------
# User Inputs
# ------------------------------------------------------------

name = st.text_input("Name")

age = st.number_input("Age", 10, 100)

height = st.number_input("Height (inches)", 48, 90)

weight = st.number_input("Weight (kg)", 30.0, 200.0)

bmi_auto = calculate_bmi(weight, height)

bmi = st.number_input(
    "BMI",
    value=float(bmi_auto)
)

bodyfat = st.number_input("Body Fat %", 1.0, 60.0)

muscle = st.number_input("Muscle Mass", 10.0, 100.0)

visceral = st.number_input("Visceral Fat", 1.0, 50.0)

bodywater = st.number_input("Body Water %", 1.0, 80.0)

# ------------------------------------------------------------
# Save Report
# ------------------------------------------------------------

if st.button("Save Report"):

    if not name:

        st.error("Name required")

    else:

        photo_path = None

        # Save selfie if uploaded
        if image:

            os.makedirs("profiles", exist_ok=True)

            filename = str(uuid.uuid4()) + ".jpg"

            photo_path = f"profiles/{filename}"

            image.save(photo_path)

        report = {
            "Name": name,
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Photo": photo_path,
            "Age": age,
            "Height": height,
            "Weight": weight,
            "BMI": bmi,
            "BodyFat": bodyfat,
            "MuscleMass": muscle,
            "VisceralFat": visceral,
            "BodyWater": bodywater
        }

        save_report(name, report)

        st.success("Report saved successfully")