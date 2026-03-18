# ============================================================
# FitCom - Sidebar Navigation (SyntraAI Styled)
# Author: Anand Kumar
#
# Purpose:
# Provides a clean, consistent navigation experience across the app.
#
# Design Notes:
# - Replaces default Streamlit navigation
# - Uses dark theme for premium SaaS feel
# - Keeps UI minimal, distraction-free
# - Built to scale as more pages/features are added
# ============================================================

import streamlit as st


def render_sidebar():

    # -------------------------------------------------------
    # GLOBAL SIDEBAR STYLING
    # -------------------------------------------------------
    # Why this exists:
    # - Streamlit default sidebar looks basic
    # - We override it to match SyntraAI branding
    # - Ensures consistent UX across all pages
    # -------------------------------------------------------

    st.markdown("""
    <style>

    /* Hide default Streamlit navigation */
    div[data-testid="stSidebarNav"] {
        display: none;
    }

    /* Remove extra top padding (fix logo spacing issue) */
    section[data-testid="stSidebar"] > div {
        padding-top: 0rem;
    }

    /* -------------------------------------------------- */
    /* SIDEBAR BACKGROUND (SyntraAI dark theme) */
    /* -------------------------------------------------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2F343A, #1F2428);
        color: white;
    }

    /* -------------------------------------------------- */
    /* MENU BUTTON STYLE */
    /* -------------------------------------------------- */
    button[kind="secondary"] {
        width: 100%;
        text-align: left;
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 6px;
        color: white;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    /* Hover effect (subtle premium feel) */
    button[kind="secondary"]:hover {
        background-color: rgba(255, 255, 255, 0.08);
        transform: translateX(3px);
    }

    /* Active click feel */
    button[kind="secondary"]:active {
        transform: scale(0.98);
    }

    /* Divider styling */
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
    # - Anchored at top
    # - Slight margin tweak removes unwanted spacing
    # - Keeps branding visible across all pages
    # -------------------------------------------------------

    st.sidebar.markdown(
        "<div style='margin-top:-10px;'>",
        unsafe_allow_html=True
    )

    st.sidebar.image("logo.png", use_column_width=True)

    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # MAIN NAVIGATION MENU
    # -------------------------------------------------------
    # Why page_link:
    # - Native Streamlit navigation
    # - Cleaner than buttons or radio
    # - Scales well with multiple pages
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
    # FOOTER / SUPPORT SECTION
    # -------------------------------------------------------
    # Keeps it minimal to avoid clutter
    # Can later include:
    # - Version info
    # - Help links
    # - Logout (if auth added)
    # -------------------------------------------------------

    st.sidebar.caption("📧 manandkumar@gmail.com")