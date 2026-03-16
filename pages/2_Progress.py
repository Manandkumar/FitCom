import streamlit as st
import pandas as pd
import os

FILE_NAME = "fitcom_reports.csv"

st.title("📈 Progress Tracking")

if not os.path.exists(FILE_NAME):

    st.info("No reports available.")

else:

    df = pd.read_csv(FILE_NAME)

    user = st.selectbox("Select User", df["Name"].unique())

    user_df = df[df["Name"] == user].sort_values("Date")

    st.dataframe(user_df)

    if len(user_df) > 1:

        st.line_chart(
            user_df.set_index("Date")[["Weight","BodyFat","MuscleMass"]]
        )