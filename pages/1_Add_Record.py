# ============================================================
# FitCom - Add My Fitness Record (Final Fixed)
# ============================================================

import streamlit as st
from datetime import datetime

from storage import save_report
from storage.supabase_storage import upload_image
from sidebar import render_sidebar


# ============================================================
# HEALTH SCORE FUNCTION
# ============================================================

def calculate_health_score(data):
    score = 0

    bmi = data.get("BMI", 0)
    if 18.5 <= bmi <= 24.9:
        score += 20
    elif 25 <= bmi <= 29.9:
        score += 10

    bf = data.get("BodyFat", 0)
    if 10 <= bf <= 20:
        score += 20
    elif 20 < bf <= 25:
        score += 10

    if data.get("MuscleMass", 0) >= 40:
        score += 15

    if data.get("VisceralFat", 0) < 10:
        score += 15

    if data.get("BMR", 0) >= 1200:
        score += 10

    if 50 <= data.get("Weight", 0) <= 90:
        score += 10

    return min(score, 100)


# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(page_title="Add My Record", layout="wide")
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
    age = st.number_input("Age", min_value=10, max_value=100, value=25)

with col2:
    height_in = st.number_input("Height (inches)", min_value=36.0, max_value=100.0, value=65.0)
    height = height_in * 2.54

with col3:
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)

# ============================================================
# BODY METRICS
# ============================================================

st.subheader("📊 Body Composition")

col1, col2, col3 = st.columns(3)

with col1:
    height_m = height / 100 if height > 0 else 1
    bmi = round(weight / (height_m ** 2), 2)
    st.metric("BMI", bmi)

with col2:
    bodyfat = st.number_input("Body Fat (%)", 1.0, 60.0, value=18.0)

with col3:
    muscle_mass = st.number_input("Muscle Mass", 10.0, 100.0, value=40.0)

# ============================================================
# EXTRA METRICS
# ============================================================

st.subheader("⚙️ Additional Metrics")

col1, col2 = st.columns(2)

with col1:
    visceral_fat = st.number_input("Visceral Fat", 1.0, 30.0, value=8.0)

with col2:
    bmr = st.number_input("BMR", 500.0, 4000.0, value=1500.0)

# ============================================================
# HIIT TRAINING
# ============================================================

st.markdown("---")
st.subheader("🔥 HIIT Training")

col1, col2, col3 = st.columns(3)

with col1:
    hiit_date = st.date_input("Session Date")

with col2:
    session_no = st.number_input("Session Number", min_value=1, value=1)

with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, value=30)

st.markdown("### Optional Performance")

running_distance = st.number_input("Running (km)", value=0.0)
sledge_push = st.number_input("Sledge Push (kg)", value=0.0)
sledge_pull = st.number_input("Sledge Pull (kg)", value=0.0)
lunge_walk = st.number_input("Lunge Walk (kg)", value=0.0)
farmers_carry = st.number_input("Farmers Carry (kg)", value=0.0)
box_jump = st.number_input("Box Jumps", value=0)
wall_ball = st.number_input("Wall Balls", value=0)

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

st.markdown("---")

if st.button("💾 Save Record", use_container_width=True):

    if duration <= 0:
        st.error("Duration is mandatory")
        st.stop()

    health_score = calculate_health_score({
        "BMI": bmi,
        "BodyFat": bodyfat,
        "MuscleMass": muscle_mass,
        "VisceralFat": visceral_fat,
        "BMR": bmr,
        "Weight": weight
    })

    # Health interpretation
    if health_score >= 75:
        status = "🔥 Excellent"
    elif health_score >= 50:
        status = "👍 Good"
    else:
        status = "⚠️ Needs Improvement"

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

        "HealthScore": health_score,
        "HealthStatus": status,

        "HIIT": {
            "Date": str(hiit_date),
            "SessionNo": session_no,
            "Duration": duration,
            "RunningDistance": running_distance,
            "SledgePush": sledge_push,
            "SledgePull": sledge_pull,
            "LungeWalk": lunge_walk,
            "FarmersCarry": farmers_carry,
            "BoxJump": box_jump,
            "WallBall": wall_ball
        },

        "IsDeleted": False
    }

    save_report(user, report)

    st.success("Record saved successfully ✅")
    st.metric("Health Score", health_score)
    st.write(f"Status: {status}")