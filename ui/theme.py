# ============================================================
# FitCom - UI Theme
# Author: Anand Kumar
#
# Purpose:
# Centralized styling for the entire application.
#
# Why this matters:
# - Ensures consistent UI across all pages
# - Eliminates repeated CSS
# - Enables quick design changes globally
# ============================================================

import streamlit as st


def apply_theme():
    st.markdown("""
    <style>

    /* =======================================================
       GLOBAL BASE
    ======================================================= */

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: #2C2C2C;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* =======================================================
       HEADINGS
    ======================================================= */

    h1, h2, h3 {
        margin-bottom: 6px !important;
        font-weight: 600;
    }

    h2 {
        font-size: 22px !important;
    }

    h3 {
        font-size: 18px !important;
    }

    /* =======================================================
       LABELS & INPUTS
    ======================================================= */

    label {
        font-size: 13px !important;
        font-weight: 500 !important;
        margin-bottom: 2px !important;
    }

    input, select {
        height: 36px !important;
        padding: 6px !important;
        font-size: 14px !important;
    }

    div[data-baseweb="input"] {
        height: 36px !important;
    }

    /* Reduce spacing between inputs */
    .stNumberInput, .stTextInput, .stSelectbox {
        margin-bottom: 8px !important;
    }

    /* =======================================================
       BUTTONS
    ======================================================= */

    button {
        border-radius: 8px !important;
        font-size: 14px !important;
        padding: 6px 12px !important;
    }

    button[kind="primary"] {
        background-color: #1FA7A1 !important;
        color: white !important;
        border: none;
    }

    button[kind="primary"]:hover {
        background-color: #178f8a !important;
    }

    /* =======================================================
       METRICS
    ======================================================= */

    div[data-testid="metric-container"] {
        background: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.04);
    }

    div[data-testid="metric-container"] label {
        font-size: 12px !important;
        color: #6c757d;
    }

    div[data-testid="metric-container"] div {
        font-size: 16px !important;
        font-weight: 600;
    }

    /* =======================================================
       CARD SYSTEM (CORE DESIGN)
    ======================================================= */

    .card {
        background: white;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 14px;
    }

    /* =======================================================
       TABLE STYLING (Leaderboard)
    ======================================================= */

    table {
        border-collapse: separate !important;
        border-spacing: 0 10px;
        font-size: 14px !important;
    }

    thead th {
        text-align: center !important;
        background: #f4f6f8;
        padding: 10px !important;
        border: none !important;
    }

    tbody tr {
        background: white;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
    }

    tbody td {
        padding: 10px !important;
        border: none !important;
        text-align: center;
    }

    /* Rounded rows */
    tbody tr td:first-child {
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
    }

    tbody tr td:last-child {
        border-top-right-radius: 10px;
        border-bottom-right-radius: 10px;
    }

    /* =======================================================
       IMAGE STYLING
    ======================================================= */

    img {
        border-radius: 8px;
    }

    /* =======================================================
       INDICATORS
    ======================================================= */

    .indicator {
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }

    /* =======================================================
       DIVIDER
    ======================================================= */

    hr {
        border: none;
        height: 1px;
        background: #e0e0e0;
        margin: 12px 0;
    }

    </style>
    """, unsafe_allow_html=True)