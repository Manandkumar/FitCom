import streamlit as st
import pandas as pd
import os

from sidebar import render_sidebar
from ui.theme import apply_theme
from ui.components import page_header, section, card_start, card_end

# -------------------------------------------------------
# INIT
# -------------------------------------------------------

render_sidebar()
apply_theme()

FILE_NAME = "fitcom_reports.csv"

page_header("Progress Tracking", "Track member progress over time")

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

if not os.path.exists(FILE_NAME):
    st.info("No reports available.")
    st.stop()

df = pd.read_csv(FILE_NAME)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# -------------------------------------------------------
# USER SELECTION (CARD)
# -------------------------------------------------------

section("Select Member")

card_start()

users = sorted(df["Name"].unique())
user = st.selectbox("Choose Member", users)

card_end()

# -------------------------------------------------------
# FILTER DATA
# -------------------------------------------------------

user_df = df[df["Name"] == user].sort_values("Date")
user_display = user_df.drop(columns=["Age"], errors="ignore")

# -------------------------------------------------------
# TABLE (CARD)
# -------------------------------------------------------

section("Progress History")

card_start()
st.dataframe(user_display, use_container_width=True)
card_end()

# -------------------------------------------------------
# CHART (CARD)
# -------------------------------------------------------

if len(user_df) > 1:

    section("Progress Trend")

    card_start()

    metrics = ["Weight", "BodyFat", "MuscleMass"]
    available = [m for m in metrics if m in user_df.columns]

    if available:
        chart_df = user_df.set_index("Date")[available]
        st.line_chart(chart_df)
    else:
        st.warning("No chartable data")

    card_end()

else:
    st.info("Add more entries to see trends")