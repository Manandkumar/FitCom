import streamlit as st
import pandas as pd
import os
from sidebar import render_sidebar
render_sidebar()

FILE_NAME = "fitcom_reports.csv"

st.title("🤖 AI Health Coach")

def ai_coach(row):

    tips=[]

    if row["BMI"]>25:
        tips.append("BMI slightly high. Focus on fat reduction.")

    if row["BodyFat"]>20:
        tips.append("Body fat above optimal. Add cardio.")

    if not tips:
        tips.append("Your body composition is healthy.")

    return tips

if os.path.exists(FILE_NAME):

    df=pd.read_csv(FILE_NAME)

    user=st.selectbox("Select User",df["Name"].unique())

    latest=df[df["Name"]==user].iloc[-1]

    st.write(latest)

    tips=ai_coach(latest)

    for tip in tips:
        st.success(tip)