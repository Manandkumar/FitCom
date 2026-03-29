# styles.py

import streamlit as st

def apply_global_styles():
    st.markdown("""
    <style>

    /* GLOBAL FONT */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
    }

    /* MAIN CONTAINER */
    .block-container {
        padding: 2rem 2rem;
    }

    /* METRIC CARDS */
    div[data-testid="metric-container"] {
        padding: 12px;
        border-radius: 10px;
        background-color: #f7f7f7;
    }

    /* HEADINGS */
    h1, h2, h3 {
        font-weight: 600;
    }

    </style>
    """, unsafe_allow_html=True)