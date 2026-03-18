# ============================================================
# FitCom - Sidebar Navigation (SyntraAI Clean Theme)
# Author: Anand Kumar
#
# Purpose:
# Provides a clean, minimal, and consistent navigation panel
# across all pages of the FitCom application.
#
# Design Philosophy:
# - Light UI for better readability (business app feel)
# - Teal accents aligned with SyntraAI branding
# - Subtle interactions (hover, active states)
# - Keep it simple and distraction-free
# ============================================================

import streamlit as st


def render_sidebar():

    # -------------------------------------------------------
    # GLOBAL SIDEBAR STYLING
    # -------------------------------------------------------
    # Why this block exists:
    # - Streamlit's default sidebar looks very plain
    # - We override styles to match a modern SaaS look
    # - Also fixes spacing and improves readability
    # -------------------------------------------------------

    st.markdown("""
    <style>

    /* Hide default Streamlit page navigation */
    div[data-testid="stSidebarNav"] {
        display: none;
    }

    /* Sidebar background + subtle border */
    section[data-testid="stSidebar"] {
        background-color: #F4F6F8;
        border-right: 1px solid #e0e0e0;
    }

    /* Remove extra padding at top (fix logo spacing) */
    section[data-testid="stSidebar"] > div {
        padding-top: 0rem;
    }

    /* -------------------------------------------------- */
    /* TEXT STYLING */
    /* -------------------------------------------------- */
    /* Force consistent readable text across sidebar */
    section[data-testid="stSidebar"] * {
        color: #2C2C2C !important;
        font-size: 14px;
    }

    /* -------------------------------------------------- */
    /* NAVIGATION LINKS (page_link renders <a>) */
    /* -------------------------------------------------- */
    section[data-testid="stSidebar"] a {
        display: block;
        padding: 10px 12px;
        margin-bottom: 6px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    /* Hover interaction */
    section[data-testid="stSidebar"] a:hover {
        background: rgba(31,167,161,0.1);
        color: #1FA7A1 !important;
        transform: translateX(3px);
    }

    /* Active page highlight */
    section[data-testid="stSidebar"] a[aria-current="page"] {
        background: rgba(31,167,161,0.15);
        color: #1FA7A1 !important;
        font-weight: 600;
    }

    /* Divider styling */
    hr {
        border: none;
        height: 1px;
        background: #e0e0e0;
    }

    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------
    # LOGO SECTION
    # -------------------------------------------------------
    # Notes:
    # - Keep it simple (no background box → cleaner look)
    # - Slight padding so it doesn't feel cramped
    # - Works best with transparent PNG logo
    # -------------------------------------------------------

    st.sidebar.markdown(
        "<div style='padding:10px 5px 10px 5px;'>",
        unsafe_allow_html=True
    )

    st.sidebar.image("logo.png", use_column_width=True)

    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # MAIN NAVIGATION MENU
    # -------------------------------------------------------
    # Using page_link instead of buttons:
    # - Native Streamlit navigation
    # - Cleaner UX
    # - Automatically handles routing between pages
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
        label="➕ Add New Member"
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
    # FOOTER SECTION
    # -------------------------------------------------------
    # Minimal for now:
    # - Can later include version info, logout, help links
    # - Keeping it clean avoids clutter
    # -------------------------------------------------------

    st.sidebar.caption("📧 manandkumar@gmail.com")