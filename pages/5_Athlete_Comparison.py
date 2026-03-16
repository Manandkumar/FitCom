# ============================================================
# FitCom - Athlete Comparison
# Author: Anand Kumar
# ============================================================

import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

FILE_NAME = "fitcom_reports.csv"

st.title("🏅 Athlete Comparison")

# ------------------------------------------------------------
# Load Dataset
# ------------------------------------------------------------

if not os.path.exists(FILE_NAME):

    st.info("No reports available yet.")

else:

    df = pd.read_csv(FILE_NAME)

    athletes = df["Name"].unique()

    selected = st.multiselect(
        "Select athletes to compare",
        athletes,
        default=athletes[:2] if len(athletes) >= 2 else athletes
    )

    if len(selected) == 0:

        st.info("Select at least one athlete.")

    else:

        compare_df = df[df["Name"].isin(selected)]

        # Latest report per athlete
        latest = (
            compare_df
            .sort_values("Date")
            .groupby("Name")
            .tail(1)
            .set_index("Name")
        )

        st.subheader("Latest Metrics")

        st.dataframe(latest)

        # ------------------------------------------------------------
        # Bar Chart Comparison
        # ------------------------------------------------------------

        st.subheader("Metric Comparison")

        metrics = ["BMI", "BodyFat", "MuscleMass", "BodyWater", "VisceralFat"]

        st.bar_chart(latest[metrics])

        # ------------------------------------------------------------
        # Radar Chart Comparison
        # ------------------------------------------------------------

        st.subheader("Body Composition Radar")

        fig = go.Figure()

        for athlete in latest.index:

            fig.add_trace(go.Scatterpolar(
                r=[
                    latest.loc[athlete]["BMI"],
                    latest.loc[athlete]["BodyFat"],
                    latest.loc[athlete]["MuscleMass"],
                    latest.loc[athlete]["BodyWater"],
                    latest.loc[athlete]["VisceralFat"]
                ],
                theta=[
                    "BMI",
                    "Body Fat",
                    "Muscle Mass",
                    "Body Water",
                    "Visceral Fat"
                ],
                fill="toself",
                name=athlete
            ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)