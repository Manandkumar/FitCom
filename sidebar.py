# ============================================================
# FitCom - Sidebar Navigation (SyntraAI Styled)
# Author: Anand Kumar
#
# Purpose:
# Clean, readable, dark-themed sidebar with proper contrast
# ============================================================

import streamlit as st


def render_sidebar():

    # -------------------------------------------------------
    # GLOBAL SIDEBAR STYLING (FINAL FIX)
    # -------------------------------------------------------

    st.markdown("""
    <style>

    /* Hide default navigation */
    div[data-testid="stSidebarNav"] {
        display: none;
    }

    /* Remove top padding */
    section[data-testid="stSidebar"] > div {
        padding-top: 0rem;
    }

    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2F343A, #1F2428);
    }

    /* 🔥 FORCE TEXT VISIBILITY (important fix) */
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
        opacity: 1 !important;
    }

    /* -------------------------------------------------- */
    /* 🔥 FIX page_link (THIS WAS THE ISSUE) */
    /* -------------------------------------------------- */
    section[data-testid="stSidebar"] a {
        display: block;
        padding: 10px 12px;
        margin-bottom: 6px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 500;
        color: #FFFFFF !important;
        transition: all 0.2s ease;
    }

    /* Hover */
    section[data-testid="stSidebar"] a:hover {
        background: rgba(255,255,255,0.08);
        transform: translateX(3px);
    }

    /* Active page */
    section[data-testid="stSidebar"] a[aria-current="page"] {
        background: rgba(255,255,255,0.15);
        font-weight: 600;
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: rgba(255,255,255,0.1);
    }

    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------
    # LOGO SECTION
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