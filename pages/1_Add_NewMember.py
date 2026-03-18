from sidebar import render_sidebar
from ui.theme import apply_theme
from ui.components import page_header, section, card_start, card_end

import streamlit as st
import uuid, os
from PIL import Image
from datetime import datetime
from storage import save_report

render_sidebar()
apply_theme()

page_header("Add Member", "Capture body composition")

# --- Utils ---
def calculate_bmi(w,h): return round(w/((h*0.0254)**2),2) if h else 0

def save_image(f):
    try:
        img = Image.open(f).convert("RGB")
        os.makedirs("profiles", exist_ok=True)
        path = f"profiles/{uuid.uuid4()}.jpg"
        img.save(path)
        return path, img
    except: return None, None

# --- Profile ---
section("User Profile")
card_start()

col1,col2 = st.columns([1,2])
with col1:
    up = st.file_uploader("Photo")
    photo=None
    if up:
        photo,img = save_image(up)
        st.image(img,width=120)

with col2:
    name = st.text_input("Name")
    gender = st.selectbox("Gender",["Male","Female"])
    age = st.number_input("Age",10,100)
    height = st.number_input("Height (inches)",48,90)

card_end()

# --- Body ---
section("Body Composition")
card_start()

col1,col2,col3 = st.columns(3)
with col1:
    weight = st.number_input("Weight",30.0,200.0)
    bmi = calculate_bmi(weight,height)
    st.metric("BMI",bmi)

with col2:
    bodyfat = st.number_input("Body Fat",1.0,60.0)

with col3:
    muscle = st.number_input("Muscle",10.0,100.0)

card_end()

# --- Save ---
if st.button("Save Report",use_container_width=True):
    if not name:
        st.error("Name required")
    else:
        save_report(name,{
            "Name":name,"Gender":gender,"Age":age,
            "Height":height,"Weight":weight,
            "BMI":bmi,"BodyFat":bodyfat,"MuscleMass":muscle,
            "Photo":photo,"Date":datetime.now().strftime("%Y-%m-%d")
        })
        st.success("Saved ✅")