# ============================================================
# FitCom - Sidebar Navigation (Final Polished Version)
# Author: Anand Kumar
# ============================================================

import streamlit as st


def render_sidebar():

    # -------------------------------------------------------
    # GLOBAL STYLING
    # -------------------------------------------------------

    st.markdown("""
    <style>

    /* Hide default navigation */
    div[data-testid="stSidebarNav"] {
        display: none;
    }

    /* Sidebar base */
    section[data-testid="stSidebar"] {
        background-color: #F7F9FB;
        border-right: 1px solid #E6EAF0;
    }

    /* Remove top padding */
    section[data-testid="stSidebar"] > div {
        padding-top: 0rem;
    }

    /* Text */
    section[data-testid="stSidebar"] * {
        color: #2C2C2C !important;
        font-size: 14px;
    }

    /* -------------------------------------------------- */
    /* LOGO */
    /* -------------------------------------------------- */
    .logo-box {
        padding: 12px 10px;
        border-bottom: 1px solid #E6EAF0;
        margin-bottom: 8px;
    }

    /* -------------------------------------------------- */
    /* NAV LINKS */
    /* -------------------------------------------------- */
    section[data-testid="stSidebar"] a {
        display: block;
        padding: 10px 12px;
        margin: 4px 0;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.15s ease;
    }

    /* Hover */
    section[data-testid="stSidebar"] a:hover {
        background: rgba(31,167,161,0.08);
        color: #1FA7A1 !important;
    }

    /* Active (STRONG FIX) */
    section[data-testid="stSidebar"] a[aria-current="page"] {
        background: #1FA7A1 !important;
        color: white !important;
        font-weight: 600;
        box-shadow: 0 2px 6px rgba(31,167,161,0.25);
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: #E6EAF0;
        margin: 10px 0;
    }

    /* Footer */
    .footer {
        font-size: 12px;
        color: #888;
        margin-top: 10px;
    }

    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------
    # LOGO
    # -------------------------------------------------------

    st.sidebar.markdown("<div class='logo-box'>", unsafe_allow_html=True)
    st.sidebar.image("logo.png", width="stretch")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------
    # MAIN NAVIGATION
    # -------------------------------------------------------

    st.sidebar.page_link("Dashboard.py", label="🏠 Dashboard")

    st.sidebar.page_link(
        "pages/9_Member_Dashboard.py",
        label="👤 Individual Board"
    )

    st.sidebar.page_link(
        "pages/2_Progress.py",
        label="📊 Progress"
    )

    st.sidebar.page_link(
        "pages/1_Add_NewMember.py",
        label="➕ Add Member"
    )

    st.sidebar.page_link(
        "pages/3_Leaderboard.py",
        label="🏆 Leaderboard"
    )

    st.sidebar.page_link(
        "pages/4_AI_Coach.py",
        label="🤖 AI Coach"
    )

    st.sidebar.page_link(
        "pages/5_Athlete_Comparison.py",
        label="⚖️ Comparison"
    )

    st.sidebar.page_link(
        "pages/6_Edit_Report.py",
        label="✏️ Edit Report"
    )

    st.sidebar.page_link(
        "pages/8_Weekly_Report.py",
        label="📅 Weekly Report"
    )

    st.sidebar.page_link(
        "pages/7_Admin_Dashboard.py",
        label="⚙️ Admin"
    )

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # FOOTER
    # -------------------------------------------------------

    st.sidebar.markdown(
        "<div class='footer'>📧 manandkumar@gmail.com</div>",
        unsafe_allow_html=True
    )