# ============================================================
# FitCom - Ultra Clean Sidebar
# ============================================================

import streamlit as st

def render_sidebar():

    # Hide default navigation
    st.markdown("""
    <style>
    div[data-testid="stSidebarNav"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

    # -------------------------
    # LOGO
    # -------------------------

    st.sidebar.image("logo.png", width=110)
    st.sidebar.markdown(
        "<p style='text-align:center; font-weight:600;'>SyntraAI</p>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown("---")

    # -------------------------
    # MAIN NAV (ONLY 3)
    # -------------------------

    if st.sidebar.button("🏠 Dashboard"):
        st.switch_page("Dashboard.py")

    if st.sidebar.button("📊 Progress"):
        st.switch_page("pages/2_Progress.py")

    if st.sidebar.button("➕ Add"):
        st.switch_page("pages/1_Add_NewMember.py")

    st.sidebar.markdown("---")

    # -------------------------
    # SINGLE DROPDOWN FOR REST
    # -------------------------

    option = st.sidebar.selectbox(
        "More",
        [
            "Select",
            "AI Coach",
            "Leaderboard",
            "Comparison",
            "Edit Report",
            "Weekly Report",
            "Admin Dashboard"
        ]
    )

    if option == "AI Coach":
        st.switch_page("pages/4_AI_Coach.py")

    elif option == "Leaderboard":
        st.switch_page("pages/3_Leaderboard.py")

    elif option == "Comparison":
        st.switch_page("pages/5_Athlete_Comparison.py")

    elif option == "Edit Report":
        st.switch_page("pages/6_Edit_Report.py")

    elif option == "Weekly Report":
        st.switch_page("pages/8_Weekly_Report.py")

    elif option == "Admin Dashboard":
        st.switch_page("pages/7_Admin_Dashboard.py")