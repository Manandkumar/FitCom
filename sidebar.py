# ============================================================
# FitCom - Sidebar Navigation (Organized + Branding)
# ============================================================

import streamlit as st

def render_sidebar():

    # -------------------------------------------------------
    # LOGO + BRANDING
    # -------------------------------------------------------

    st.sidebar.markdown(
        "<div style='text-align:center;'>",
        unsafe_allow_html=True
    )

    st.sidebar.image("logo.png", width=120)

    st.sidebar.markdown(
        "<h4 style='margin-bottom:0;'>SyntraAI</h4>",
        unsafe_allow_html=True
    )

    st.sidebar.caption("Track • Transform • Progress")

    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # MEMBER SECTION
    # -------------------------------------------------------

    st.sidebar.markdown("## 👤 Member")

    st.sidebar.page_link(
        "pages/2_Progress.py",
        label="My Progress"
    )

    st.sidebar.page_link(
        "pages/8_Weekly_Report.py",
        label="Weekly Report"
    )

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # TRAINER SECTION
    # -------------------------------------------------------

    st.sidebar.markdown("## 🏋️ Trainer")

    st.sidebar.page_link(
        "pages/1_Add_NewMember.py",
        label="Add Member / Report"
    )

    st.sidebar.page_link(
        "pages/6_Edit_Report.py",
        label="Edit Report"
    )

    st.sidebar.page_link(
        "pages/3_Leaderboard.py",
        label="Leaderboard"
    )

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # AI FEATURES
    # -------------------------------------------------------

    st.sidebar.markdown("## 🤖 AI Features")

    st.sidebar.page_link(
        "pages/4_AI_Coach.py",
        label="AI Coach"
    )

    st.sidebar.page_link(
        "pages/5_Athlete_Comparison.py",
        label="Athlete Comparison"
    )

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # ADMIN SECTION
    # -------------------------------------------------------

    st.sidebar.markdown("## ⚙️ Admin")

    st.sidebar.page_link(
        "pages/7_Admin_Dashboard.py",
        label="Admin Dashboard"
    )

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