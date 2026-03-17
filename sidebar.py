# ============================================================
# FitCom - Sidebar Navigation (FINAL WORKING VERSION)
# ============================================================

import streamlit as st

def render_sidebar():

    # -------------------------------------------------------
    # 🔥 FORCE HIDE STREAMLIT DEFAULT NAVIGATION
    # -------------------------------------------------------

    st.markdown("""
    <style>

    /* Hide default multipage navigation */
    div[data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Remove extra padding at top */
    div[data-testid="stSidebarContent"] {
        padding-top: 0rem;
    }

    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------
    # 🧠 LOGO + BRANDING (TOP FIXED)
    # -------------------------------------------------------

    st.sidebar.image("logo.png", width=130)

    st.sidebar.markdown(
        "<h4 style='text-align:center; margin-top:-10px;'>SyntraAI</h4>",
        unsafe_allow_html=True
    )

    st.sidebar.caption("Track • Transform • Progress")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # 👤 MEMBER SECTION
    # -------------------------------------------------------

    st.sidebar.markdown("## 👤 Member")

    if st.sidebar.button("📊 My Progress"):
        st.switch_page("pages/2_Progress.py")

    if st.sidebar.button("📅 Weekly Report"):
        st.switch_page("pages/8_Weekly_Report.py")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # 🏋️ TRAINER SECTION
    # -------------------------------------------------------

    st.sidebar.markdown("## 🏋️ Trainer")

    if st.sidebar.button("➕ Add Member / Report"):
        st.switch_page("pages/1_Add_NewMember.py")

    if st.sidebar.button("✏️ Edit Report"):
        st.switch_page("pages/6_Edit_Report.py")

    if st.sidebar.button("🏆 Leaderboard"):
        st.switch_page("pages/3_Leaderboard.py")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # 🤖 AI FEATURES
    # -------------------------------------------------------

    st.sidebar.markdown("## 🤖 AI Features")

    if st.sidebar.button("🧠 AI Coach"):
        st.switch_page("pages/4_AI_Coach.py")

    if st.sidebar.button("⚖️ Athlete Comparison"):
        st.switch_page("pages/5_Athlete_Comparison.py")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # ⚙️ ADMIN SECTION
    # -------------------------------------------------------

    st.sidebar.markdown("## ⚙️ Admin")

    if st.sidebar.button("📋 Admin Dashboard"):
        st.switch_page("pages/7_Admin_Dashboard.py")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # 📞 SUPPORT
    # -------------------------------------------------------

    st.sidebar.markdown("### Need Help?")

    st.sidebar.markdown(
        """
        **Anand Kumar**  
        📧 manandkumar@gmail.com
        """
    )