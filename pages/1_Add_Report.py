```python
import streamlit as st
import pandas as pd
import uuid
from PIL import Image
import os
from datetime import datetime
from storage import save_report
from sidebar import render_sidebar

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------

render_sidebar()

st.title("➕ Add Body Composition Report")

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------

FILE_NAME = "fitcom_reports.csv"

# ------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------

def calculate_bmi(weight, height_in):
    """Calculate BMI using weight (kg) and height (inches)"""

    if height_in == 0:
        return 0

    height_m = height_in * 0.0254
    bmi = weight / (height_m ** 2)

    return round(bmi, 2)


def save_uploaded_image(uploaded_file):
    """
    Save uploaded image safely
    Handles RGBA / PNG images correctly
    """

    try:

        image = Image.open(uploaded_file)

        # Convert incompatible modes
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        os.makedirs("profiles", exist_ok=True)

        filename = f"{uuid.uuid4()}.jpg"

        path = os.path.join("profiles", filename)

        image.save(path, format="JPEG")

        return path, image

    except Exception as e:

        st.error("Error saving image")

        return None, None


# ------------------------------------------------------------
# Selfie Upload Section
# ------------------------------------------------------------

st.subheader("User Profile")

uploaded_selfie = st.file_uploader(
    "Upload Selfie",
    type=["jpg", "jpeg", "png"]
)

photo_path = None
preview_image = None

if uploaded_selfie:

    photo_path, preview_image = save_uploaded_image(uploaded_selfie)

    if preview_image:
        st.image(preview_image, width=200)


# ------------------------------------------------------------
# User Inputs
# ------------------------------------------------------------

st.subheader("Body Composition Data")

name = st.text_input("Name")

age = st.number_input(
    "Age",
    min_value=10,
    max_value=100,
    value=25
)

height = st.number_input(
    "Height (inches)",
    min_value=48,
    max_value=90,
    value=65
)

weight = st.number_input(
    "Weight (kg)",
    min_value=30.0,
    max_value=200.0,
    value=70.0
)

# Auto BMI Calculation
bmi = calculate_bmi(weight, height)

st.metric("Calculated BMI", bmi)

bodyfat = st.number_input(
    "Body Fat %",
    min_value=1.0,
    max_value=60.0,
    value=20.0
)

muscle = st.number_input(
    "Muscle Mass",
    min_value=10.0,
    max_value=100.0,
    value=40.0
)

visceral = st.number_input(
    "Visceral Fat",
    min_value=1.0,
    max_value=50.0,
    value=10.0
)

bodywater = st.number_input(
    "Body Water %",
    min_value=1.0,
    max_value=80.0,
    value=50.0
)

# ------------------------------------------------------------
# Save Report Button
# ------------------------------------------------------------

st.divider()

if st.button("💾 Save Report"):

    if not name:

        st.error("⚠️ Name is required")

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
            "MuscleMass": muscle,
            "VisceralFat": visceral,
            "BodyWater": bodywater
        }

        try:

            save_report(name, report)

            st.success("✅ Report saved successfully")

        except Exception as e:

            st.error("Error saving report")
```
