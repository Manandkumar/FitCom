# ============================================================
# FitCom - Add My Fitness Record
# Author: Anand Kumar
# ============================================================

import streamlit as st
from datetime import datetime

# Storage
from storage import save_report
from storage.supabase_storage import upload_image

# Sidebar
from sidebar import render_sidebar


# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(page_title="Add My Record", layout="wide")

render_sidebar()

# ============================================================
# USER VALIDATION
# ============================================================

user = st.session_state.get("user")

if not user:
    st.error("Please login first")
    st.stop()

st.title("➕ Add My Fitness Record")
st.caption("Track your body metrics and progress")

st.markdown("---")

# ============================================================
# USER INFO (AUTO-FILLED)
# ============================================================

st.subheader("👤 User")

st.text_input("User", value=user, disabled=True)

# ============================================================
# BASIC DETAILS
# ============================================================

st.subheader("📋 Basic Details")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age", min_value=10, max_value=100)

with col2:
    height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0)

with col3:
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0)

# ============================================================
# BODY METRICS
# ============================================================

st.subheader("📊 Body Composition")

col1, col2, col3 = st.columns(3)

with col1:
    bmi = st.number_input("BMI", min_value=10.0, max_value=50.0)

with col2:
    bodyfat = st.number_input("Body Fat (%)", min_value=1.0, max_value=60.0)

with col3:
    muscle_mass = st.number_input("Muscle Mass", min_value=10.0, max_value=100.0)

# ============================================================
# EXTRA METRICS
# ============================================================

st.subheader("⚙️ Additional Metrics")

col1, col2 = st.columns(2)

with col1:
    visceral_fat = st.number_input("Visceral Fat", min_value=1.0, max_value=30.0)

with col2:
    bmr = st.number_input("BMR", min_value=500.0, max_value=4000.0)

# ============================================================
# PHOTO UPLOAD
# ============================================================

st.subheader("📸 Upload Photo")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

image_url = None

if uploaded_file:
    image_url = upload_image(uploaded_file)
    if image_url:
        st.image(image_url, width=200)

# ============================================================
# SAVE DATA
# ============================================================

st.markdown("---")

if st.button("💾 Save Record", use_container_width=True):

    try:

        report = {
            "UserId": user,
            "Name": user,  # 🔥 IMPORTANT: Name = User
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

        st.success("Record saved successfully ✅")

    except Exception as e:
        st.error(f"Error: {e}")