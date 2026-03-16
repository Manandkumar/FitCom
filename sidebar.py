# ============================================================
# FitCom Sidebar
# Author: Anand Kumar
# ============================================================

import streamlit as st

def render_sidebar():

    # Sidebar background color
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            background-color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.image("logo.png", width=160)
    st.sidebar.title("FitCom")
    st.sidebar.markdown("---")