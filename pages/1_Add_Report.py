```python
import streamlit as st
import uuid
from PIL import Image
import os
from datetime import datetime
from storage import save_report
from sidebar import render_sidebar

# Sidebar
render_sidebar()

st.title("➕ Add Body Composition Report")

# -------------------------------
# BMI Calculation
# -------------------------------
def calculate_bmi(weight, height_in):

    if height_in == 0:
        return 0

    height_m = height_in * 0.0254
    bmi = weight / (height_m ** 2)

    return round(bmi, 2)


# -------------------------------
# Save Uploaded Image
# -------------------------------
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

    except Exception as e:

        st.error("Image saving failed")
        return None, None


# -------------------------------
# Upload Selfie
# -------------------------------
st.subheader("User Profile")

uploaded_photo = st.file_uploader(
    "Upload Selfie",
    type=["jpg", "jpeg", "png"]
)

photo_path = None
preview = None

if uploaded_photo:
    photo_path, preview = save_image(uploaded_photo)

    if preview:
        st.image(preview, width=200)


# -------------------------------
# User Inputs
# -------------------------------
name = st.text_input("Name")

age = st.number_input("Age", 10, 100)

height = st.number_input("Height (inches)", 48, 90)

weight = st.number_input("Weight (kg)", 30.0, 200.0)

bmi = calculate_bmi(weight, height)

st.metric("BMI", bmi)

bodyfat = st.number_input("Body Fat %", 1.0, 60.0)

muscle = st.number_input("Muscle Mass", 10.0, 100.0)

visceral = st.number_input("Visceral Fat", 1.0, 50.0)

bodywater = st.number_input("Body Water %", 1.0, 80.0)


# -------------------------------
# Save Report
# -------------------------------
if st.button("Save Report"):

    if not name:

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
            "MuscleMass": muscle,
            "VisceralFat": visceral,
            "BodyWater": bodywater
        }

        save_report(name, report)

        st.success("Report saved successfully")
```
