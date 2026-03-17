# ============================================================
# FitCom - Sidebar Navigation (Final FIXED)
# ============================================================

import streamlit as st

def render_sidebar():

    # -------------------------------------------------------
    # 🔥 HIDE DEFAULT STREAMLIT NAVIGATION
    # -------------------------------------------------------

    st.markdown("""
    <style>
    section[data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------
    # LOGO + BRANDING (NOW AT TRUE TOP)
    # -------------------------------------------------------

    st.sidebar.image("logo.png", width=120)

    st.sidebar.markdown(
        "<h4 style='text-align:center; margin-top:-10px;'>SyntraAI</h4>",
        unsafe_allow_html=True
    )

    st.sidebar.caption("Track • Transform • Progress")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # 👤 MEMBER
    # -------------------------------------------------------

    st.sidebar.markdown("## 👤 Member")

    if st.sidebar.button("My Progress"):
        st.switch_page("pages/2_Progress.py")

    if st.sidebar.button("Weekly Report"):
        st.switch_page("pages/8_Weekly_Report.py")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # 🏋️ TRAINER
    # -------------------------------------------------------

    st.sidebar.markdown("## 🏋️ Trainer")

    if st.sidebar.button("Add Member / Report"):
        st.switch_page("pages/1_Add_NewMember.py")

    if st.sidebar.button("Edit Report"):
        st.switch_page("pages/6_Edit_Report.py")

    if st.sidebar.button("Leaderboard"):
        st.switch_page("pages/3_Leaderboard.py")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # 🤖 AI FEATURES
    # -------------------------------------------------------

    st.sidebar.markdown("## 🤖 AI Features")

    if st.sidebar.button("AI Coach"):
        st.switch_page("pages/4_AI_Coach.py")

    if st.sidebar.button("Athlete Comparison"):
        st.switch_page("pages/5_Athlete_Comparison.py")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # ⚙️ ADMIN
    # -------------------------------------------------------

    st.sidebar.markdown("## ⚙️ Admin")

    if st.sidebar.button("Admin Dashboard"):
        st.switch_page("pages/7_Admin_Dashboard.py")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # SUPPORT
    # -------------------------------------------------------

    st.sidebar.markdown("### Need Help?")

    st.sidebar.markdown(
        """
        **Anand Kumar**  
        📧 manandkumar@gmail.com
        """
    )