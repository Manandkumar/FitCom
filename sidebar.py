# ============================================================
# FitCom - Sidebar Navigation (SyntraAI Styled)
# Author: Anand Kumar
#
# Purpose:
# Provides a clean, consistent navigation experience across the app.
#
# Design Notes:
# - Dark theme aligned with SyntraAI branding
# - Fixes Streamlit default low-contrast behavior
# - Ensures readability + premium UI feel
# ============================================================

import streamlit as st


def render_sidebar():

    # -------------------------------------------------------
    # GLOBAL SIDEBAR STYLING
    # -------------------------------------------------------
    # Key Fix:
    # Streamlit applies low-opacity text colors by default.
    # We override EVERYTHING inside sidebar for proper contrast.
    # -------------------------------------------------------

    st.markdown("""
    <style>

    /* Hide default Streamlit navigation */
    div[data-testid="stSidebarNav"] {
        display: none;
    }

    /* Remove top padding (fix logo gap) */
    section[data-testid="stSidebar"] > div {
        padding-top: 0rem;
    }

    /* -------------------------------------------------- */
    /* SIDEBAR BACKGROUND */
    /* -------------------------------------------------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2F343A, #1F2428);
    }

    /* -------------------------------------------------- */
    /* FORCE TEXT VISIBILITY (CRITICAL FIX) */
    /* -------------------------------------------------- */
    section[data-testid="stSidebar"] * {
        color: #EAECEF !important;
    }

    /* -------------------------------------------------- */
    /* MENU BUTTON STYLE */
    /* -------------------------------------------------- */
    button[kind="secondary"] {
        width: 100%;
        text-align: left;
        border-radius: 10px;
        padding: 10px 12px;
        margin-bottom: 6px;
        background: transparent;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    /* Hover effect */
    button[kind="secondary"]:hover {
        background-color: rgba(255, 255, 255, 0.08);
        transform: translateX(3px);
    }

    /* Active page highlight */
    button[kind="secondary"][aria-current="page"] {
        background: rgba(255, 255, 255, 0.12);
        font-weight: 600;
    }

    /* Click feedback */
    button[kind="secondary"]:active {
        transform: scale(0.98);
    }

    /* Divider */
    hr {
        border: 0;
        height: 1px;
        background: rgba(255,255,255,0.1);
    }

    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------
    # LOGO SECTION
    # -------------------------------------------------------
    # Wrapped in soft card to avoid harsh white box look
    # -------------------------------------------------------

    st.sidebar.markdown(
        "<div style='margin-top:-10px;'>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown("""
    <div style="
        background: rgba(255,255,255,0.05);
        padding:10px;
        border-radius:12px;
        margin-bottom:10px;
    ">
    """, unsafe_allow_html=True)

    st.sidebar.image("logo.png", use_column_width=True)

    st.sidebar.markdown("</div></div>", unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # MAIN NAVIGATION
    # -------------------------------------------------------

    st.sidebar.page_link("Dashboard.py", label="🏠 Dashboard")

    st.sidebar.page_link("pages/9_Member_Dashboard.py", label="👤 Individual Board")

    st.sidebar.page_link("pages/2_Progress.py", label="📊 Progress")

    st.sidebar.page_link("pages/1_Add_NewMember.py", label="➕ Add New Member")

    st.sidebar.page_link("pages/3_Leaderboard.py", label="🏆 Leaderboard")

    st.sidebar.page_link("pages/4_AI_Coach.py", label="🤖 AI Coach")

    st.sidebar.page_link("pages/5_Athlete_Comparison.py", label="⚖️ Comparison")

    st.sidebar.page_link("pages/6_Edit_Report.py", label="✏️ Edit Report")

    st.sidebar.page_link("pages/8_Weekly_Report.py", label="📅 Weekly Report")

    st.sidebar.page_link("pages/7_Admin_Dashboard.py", label="⚙️ Admin")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # FOOTER
    # -------------------------------------------------------

    st.sidebar.caption("📧 manandkumar@gmail.com")