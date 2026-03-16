import streamlit as st
import pandas as pd
import os
from sidebar import render_sidebar

render_sidebar()

FILE_NAME = "fitcom_reports.csv"
ADMIN_CODE = "syntra123"

st.title("✏️ Edit Athlete Report")

# ------------------------------------------------------------
# Access Control
# ------------------------------------------------------------

if "authorized" not in st.session_state:
    st.session_state.authorized = False

if not st.session_state.authorized:

    code = st.text_input("Enter Admin Access Code", type="password")

    if st.button("Unlock"):

        if code == ADMIN_CODE:
            st.session_state.authorized = True
            st.success("Access granted")
        else:
            st.error("Invalid access code")

    st.stop()

# ------------------------------------------------------------
# Edit Reports Section
# ------------------------------------------------------------

if os.path.exists(FILE_NAME):

    df = pd.read_csv(FILE_NAME)

    user = st.selectbox("Select Athlete", df["Name"].unique())

    user_df = df[df["Name"] == user]

    date = st.selectbox("Select Report Date", user_df["Date"])

    record_index = df[(df["Name"] == user) & (df["Date"] == date)].index[0]

    record = df.loc[record_index]

    st.subheader("Edit Metrics")

    weight = st.number_input("Weight", value=float(record["Weight"]))
    bmi = st.number_input("BMI", value=float(record["BMI"]))
    bodyfat = st.number_input("Body Fat", value=float(record["BodyFat"]))
    muscle = st.number_input("Muscle Mass", value=float(record["MuscleMass"]))
    visceral = st.number_input("Visceral Fat", value=float(record["VisceralFat"]))
    water = st.number_input("Body Water", value=float(record["BodyWater"]))

    if st.button("Update Report"):

        df.loc[record_index, "Weight"] = weight
        df.loc[record_index, "BMI"] = bmi
        df.loc[record_index, "BodyFat"] = bodyfat
        df.loc[record_index, "MuscleMass"] = muscle
        df.loc[record_index, "VisceralFat"] = visceral
        df.loc[record_index, "BodyWater"] = water

        df.to_csv(FILE_NAME, index=False)

        st.success("Report updated successfully!")

else:

    st.info("No reports available to edit.")