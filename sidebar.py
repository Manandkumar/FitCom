# ============================================================
# FitCom - Sidebar Navigation (Styled + Grouped)
# Author: Anand Kumar
# ============================================================

import streamlit as st

def render_sidebar():

    # -------------------------------------------------------
    # Sidebar Styling
    # -------------------------------------------------------

    st.markdown(
        """
        <style>

        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #ffffff;
        }

        /* Add spacing so navigation appears below the logo */
        section[data-testid="stSidebarNav"] {
            margin-top: 120px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------------------------------
    # Logo / Title (Optional - uncomment if needed)
    # -------------------------------------------------------

    # st.sidebar.image("logo.png", width=160)
    # st.sidebar.title("FitCom")

    # -------------------------------------------------------
    # MEMBER SECTION
    # -------------------------------------------------------

    st.sidebar.markdown("## 👤 Member")

    st.sidebar.page_link(
        "pages/9_👤_Member_Dashboard.py",
        label="Dashboard"
    )

    st.sidebar.page_link(
        "pages/2_Progress.py",
        label="Progress"
    )

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # TRAINER SECTION
    # -------------------------------------------------------

    st.sidebar.markdown("## 🏋️ Trainer")

    st.sidebar.page_link(
        "pages/1_Add_Report.py",
        label="Add Report"
    )

    st.sidebar.page_link(
        "pages/3_Leaderboard.py",
        label="Leaderboard"
    )

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # SYSTEM SECTION
    # -------------------------------------------------------

    st.sidebar.markdown("## ⚙️ System")

    st.sidebar.caption("More features coming soon...")

    # -------------------------------------------------------
    # Contact / Support Section (Your Original)
    # -------------------------------------------------------

    st.sidebar.markdown("---")

    st.sidebar.markdown("### Need Help?")

    st.sidebar.markdown(
        """
        **Anand Kumar**  
        📧 manandkumar@gmail.com
        """
    )