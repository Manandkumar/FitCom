# ============================================================
# FitCom - Clean Sidebar (Logo Only + White Background)
# ============================================================

import streamlit as st

def render_sidebar():

    # -------------------------------------------------------
    # GLOBAL SIDEBAR STYLING
    # -------------------------------------------------------

    st.markdown("""
    <style>

    /* Hide default Streamlit navigation */
    div[data-testid="stSidebarNav"] {
        display: none;
    }

    /* Make full sidebar white */
    section[data-testid="stSidebar"] {
        background-color: white;
    }

    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------
    # LOGO (ONLY, NO TEXT)
    # -------------------------------------------------------

    st.sidebar.image("logo.png", width=110)

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # MAIN NAV (CLEAN)
    # -------------------------------------------------------

    if st.sidebar.button("🏠 Dashboard"):
        st.switch_page("Dashboard.py")

    if st.sidebar.button("📊 Progress"):
        st.switch_page("pages/2_Progress.py")

    if st.sidebar.button("➕ Add"):
        st.switch_page("pages/1_Add_NewMember.py")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # MORE OPTIONS (DROPDOWN)
    # -------------------------------------------------------

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

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # SUPPORT (MINIMAL)
    # -------------------------------------------------------

    st.sidebar.caption("📧 manandkumar@gmail.com")