import streamlit as st

def apply_theme():
    st.markdown("""
    <style>

    /* FONT */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* PAGE SPACING */
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
    }

    /* HEADINGS */
    h1 {font-size: 26px !important; font-weight: 600;}
    h2 {font-size: 20px !important; font-weight: 600;}
    h3 {font-size: 16px !important; font-weight: 500;}

    h1, h2, h3 {
        margin-bottom: 6px !important;
    }

    /* METRIC CARDS */
    div[data-testid="metric-container"] {
        background: #ffffff;
        border-left: 4px solid #1FA7A1;
        padding: 10px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    }

    /* BUTTONS */
    button[kind="primary"] {
        background: linear-gradient(135deg, #1FA7A1, #2EC4B6);
        border-radius: 8px;
        border: none;
    }

    </style>
    """, unsafe_allow_html=True)