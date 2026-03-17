# ============================================================
# FitCom - Sidebar (Menu List Style)
# ============================================================

import streamlit as st

def render_sidebar():

    # -------------------------------------------------------
    # STYLE (WHITE + CLEAN MENU LOOK)
    # -------------------------------------------------------

    st.markdown("""
    <style>

    /* Hide default navigation */
    div[data-testid="stSidebarNav"] {
        display: none;
    }

    /* White sidebar */
    section[data-testid="stSidebar"] {
        background-color: white;
    }

    /* Menu link style */
    .menu-item {
        padding: 10px 12px;
        border-radius: 8px;
        margin-bottom: 5px;
        cursor: pointer;
        font-size: 15px;
    }

    .menu-item:hover {
        background-color: #f1f5f9;
    }

    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------
    # LOGO
    # -------------------------------------------------------

    st.sidebar.image("logo.png", use_column_width=True)
    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # MENU LIST (LINK STYLE)
    # -------------------------------------------------------

    st.sidebar.page_link("Dashboard.py", label="🏠 Dashboard")
    st.sidebar.page_link("pages/2_Progress.py", label="📊 Progress")
    st.sidebar.page_link("pages/1_Add_NewMember.py", label="➕ Add Member")
    st.sidebar.page_link("pages/3_Leaderboard.py", label="🏆 Leaderboard")
    st.sidebar.page_link("pages/4_AI_Coach.py", label="🤖 AI Coach")
    st.sidebar.page_link("pages/5_Athlete_Comparison.py", label="⚖️ Comparison")
    st.sidebar.page_link("pages/6_Edit_Report.py", label="✏️ Edit Report")
    st.sidebar.page_link("pages/8_Weekly_Report.py", label="📅 Weekly Report")
    st.sidebar.page_link("pages/7_Admin_Dashboard.py", label="⚙️ Admin")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # SUPPORT
    # -------------------------------------------------------

    st.sidebar.caption("📧 manandkumar@gmail.com")