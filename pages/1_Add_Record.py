# ============================================================
# FitCom - Add My Fitness Record (FINAL STABLE)
# ============================================================

import streamlit as st
from datetime import datetime

from storage import save_report
from storage.database_ops import save_hiit_session
from storage.supabase_storage import upload_image
from sidebar import render_sidebar
from utils import calculate_health_score


# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(page_title="Add Record", layout="wide")
render_sidebar()

user = st.session_state.get("user")

if not user:
    st.error("Please login first")
    st.stop()

st.title("➕ Add My Fitness Record")
st.markdown("---")


# ============================================================
# INPUTS
# ============================================================

st.subheader("📋 Basic Details")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age", 10, 100, value=25)

with col2:
    height_in = st.number_input("Height (inches)", 36.0, 100.0, value=65.0)
    height = height_in * 2.54

with col3:
    weight = st.number_input("Weight (kg)", 30.0, 200.0, value=70.0)


# ============================================================
# BODY METRICS
# ============================================================

st.subheader("📊 Body Composition")

height_m = height / 100 if height > 0 else 1
bmi = round(weight / (height_m ** 2), 2)

st.metric("BMI", bmi)

bodyfat = st.number_input("Body Fat (%)", 1.0, 60.0, value=18.0)
muscle_mass = st.number_input("Muscle Mass", 10.0, 100.0, value=40.0)

visceral_fat = st.number_input("Visceral Fat", 1.0, 30.0, value=8.0)
bmr = st.number_input("BMR", 500.0, 4000.0, value=1500.0)


# ============================================================
# HIIT
# ============================================================

st.subheader("🔥 HIIT Session")

hiit_date = st.date_input("Session Date")
session_no = st.number_input("Session Number", min_value=1, value=1)
duration = st.number_input("Duration (minutes)", min_value=1, value=30)

running_distance = st.number_input("Running Distance (km)", value=0.0)
sledge_push = st.number_input("Sledge Push (kg)", value=0.0)
sledge_pull = st.number_input("Sledge Pull (kg)", value=0.0)
lunge_walk = st.number_input("Lunge Walk (kg)", value=0.0)
farmers_carry = st.number_input("Farmers Carry (kg)", value=0.0)
box_jump = st.number_input("Box Jump Count", value=0)
wall_ball = st.number_input("Wall Ball Count", value=0)


# ============================================================
# PHOTO
# ============================================================

uploaded_file = st.file_uploader("Upload Image")
image_url = None

if uploaded_file:
    image_url = upload_image(uploaded_file)
    if image_url:
        st.image(image_url, width=200)


# ============================================================
# SAVE
# ============================================================

if st.button("💾 Save Record"):

    # HEALTH SCORE
    score, status = calculate_health_score({
        "BMI": bmi,
        "BodyFat": bodyfat,
        "MuscleMass": muscle_mass,
        "VisceralFat": visceral_fat,
        "BMR": bmr,
        "Weight": weight
    })

    # REPORT
    report = {
        "UserId": user,
        "Name": user,
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Photo": image_url,

        "Age": age,
        "Height": height,
        "Weight": weight,
        "BMI": bmi,

        "BodyFat": bodyfat,
        "MuscleMass": muscle_mass,
        "VisceralFat": visceral_fat,
        "BMR": bmr,

        "IsDeleted": False
    }

    save_report(user, report)

    # HIIT (Mapped to DB)
    hiit_data = {
        "UserId": user,
        "Name": user,
        "Date": str(hiit_date),

        "Workout": f"Run:{running_distance}km | Push:{sledge_push}kg | Pull:{sledge_pull}kg | Lunge:{lunge_walk}kg",

        "Duration": duration,
        "Calories": 0,
        "HeartRate": 0,

        "Notes": f"Carry:{farmers_carry}, Box:{box_jump}, Wall:{wall_ball}",

        "IsDeleted": False
    }

    save_hiit_session(hiit_data)

    st.success("Saved successfully ✅")
    st.metric("Health Score", score)
    st.write(status)