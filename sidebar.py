# ============================================================
# FitCom - Sidebar Navigation
# Author: Anand Kumar
#
# Description:
# Custom sidebar replacing Streamlit default navigation.
# - Clean menu list (no buttons/radio)
# - Logo aligned at top (no extra gap)
# - White background for consistent UI
# ============================================================

import streamlit as st


def render_sidebar():

    # -------------------------------------------------------
    # GLOBAL STYLING
    # -------------------------------------------------------
    # 1. Hide default Streamlit sidebar navigation
    # 2. Remove top padding (fix logo spacing issue)
    # 3. Ensure full white background
    # 4. Make page links look like a clean menu
    # -------------------------------------------------------

    st.markdown("""
    <style>

    /* Hide Streamlit default page navigation */
    div[data-testid="stSidebarNav"] {
        display: none;
    }

    /* Remove top padding (fixes extra gap above logo) */
    section[data-testid="stSidebar"] > div {
        padding-top: 0rem;
    }

    /* Force white background */
    section[data-testid="stSidebar"] {
        background-color: white;
    }

    /* Make page links look like menu items */
    button[kind="secondary"] {
        width: 100%;
        text-align: left;
        border-radius: 8px;
        padding: 8px 10px;
        margin-bottom: 4px;
    }

    button[kind="secondary"]:hover {
        background-color: #f1f5f9;
    }

    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------
    # LOGO SECTION
    # -------------------------------------------------------
    # - Positioned at top
    # - No shrink, keeps aspect ratio
    # - Slight negative margin to remove gap
    # -------------------------------------------------------

    st.sidebar.markdown(
        "<div style='margin-top:-10px;'>",
        unsafe_allow_html=True
    )

    st.sidebar.image("logo.png", use_column_width=True)

    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # MAIN MENU (CLEAN LIST STYLE)
    # -------------------------------------------------------
    # Using page_link → behaves like real navigation menu
    # No buttons, no radio → clean UX
    # -------------------------------------------------------
    st.sidebar.page_link("Dashboard.py", label="🏠 Dashboard")

    st.sidebar.page_link("pages/9_Member_Dashboard.py", label="👤 Individual hboard")  # ✅ ADDED

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
    # SUPPORT SECTION (MINIMAL)
    # -------------------------------------------------------

    st.sidebar.caption("📧 manandkumar@gmail.com")