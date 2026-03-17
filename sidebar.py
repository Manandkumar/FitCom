# ============================================================
# FitCom - Sidebar (Simple & Clean)
# ============================================================

import streamlit as st

def render_sidebar():

    # -------------------------------------------------------
    # HIDE DEFAULT NAV
    # -------------------------------------------------------

    st.markdown("""
    <style>
    div[data-testid="stSidebarNav"] {display: none;}
    div[data-testid="stSidebarContent"] {padding-top: 0rem;}
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------
    # LOGO
    # -------------------------------------------------------

    st.sidebar.image("logo.png", width=120)
    st.sidebar.markdown(
        "<h4 style='text-align:center; margin-top:-10px;'>SyntraAI</h4>",
        unsafe_allow_html=True
    )
    st.sidebar.caption("Track • Transform")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # MAIN NAV (ONLY 4 CORE OPTIONS)
    # -------------------------------------------------------

    if st.sidebar.button("🏠 Dashboard"):
        st.switch_page("Dashboard.py")

    if st.sidebar.button("📊 Progress"):
        st.switch_page("pages/2_Progress.py")

    if st.sidebar.button("➕ Add Entry"):
        st.switch_page("pages/1_Add_NewMember.py")

    if st.sidebar.button("🤖 AI Coach"):
        st.switch_page("pages/4_AI_Coach.py")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # MORE (COLLAPSIBLE)
    # -------------------------------------------------------

    with st.sidebar.expander("More Options"):

        if st.button("🏆 Leaderboard"):
            st.switch_page("pages/3_Leaderboard.py")

        if st.button("⚖️ Comparison"):
            st.switch_page("pages/5_Athlete_Comparison.py")

        if st.button("✏️ Edit Report"):
            st.switch_page("pages/6_Edit_Report.py")

        if st.button("📅 Weekly Report"):
            st.switch_page("pages/8_Weekly_Report.py")

        if st.button("⚙️ Admin"):
            st.switch_page("pages/7_Admin_Dashboard.py")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # SUPPORT
    # -------------------------------------------------------

    st.sidebar.caption("Need Help?")
    st.sidebar.caption("📧 manandkumar@gmail.com")