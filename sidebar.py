# ============================================================
# FitCom - Sidebar (Menu Style - Clean)
# ============================================================

import streamlit as st

def render_sidebar():

    # -------------------------------------------------------
    # STYLE (WHITE + CLEAN)
    # -------------------------------------------------------

    st.markdown("""
    <style>

    /* Hide default Streamlit navigation */
    div[data-testid="stSidebarNav"] {
        display: none;
    }

    /* Full white sidebar */
    section[data-testid="stSidebar"] {
        background-color: white;
    }

    /* Improve spacing */
    .stRadio > div {
        gap: 8px;
    }

    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------
    # LOGO (PROPER SIZE)
    # -------------------------------------------------------

    st.sidebar.image("logo.png", use_column_width=True)

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # MENU (CLEAN RADIO NAV)
    # -------------------------------------------------------

    menu = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📊 Progress",
            "➕ Add Member",
            "🏆 Leaderboard",
            "🤖 AI Coach",
            "⚖️ Comparison",
            "✏️ Edit Report",
            "📅 Weekly Report",
            "⚙️ Admin"
        ]
    )

    # -------------------------------------------------------
    # NAVIGATION LOGIC
    # -------------------------------------------------------

    if menu == "🏠 Dashboard":
        st.switch_page("Dashboard.py")

    elif menu == "📊 Progress":
        st.switch_page("pages/2_Progress.py")

    elif menu == "➕ Add Member":
        st.switch_page("pages/1_Add_NewMember.py")

    elif menu == "🏆 Leaderboard":
        st.switch_page("pages/3_Leaderboard.py")

    elif menu == "🤖 AI Coach":
        st.switch_page("pages/4_AI_Coach.py")

    elif menu == "⚖️ Comparison":
        st.switch_page("pages/5_Athlete_Comparison.py")

    elif menu == "✏️ Edit Report":
        st.switch_page("pages/6_Edit_Report.py")

    elif menu == "📅 Weekly Report":
        st.switch_page("pages/8_Weekly_Report.py")

    elif menu == "⚙️ Admin":
        st.switch_page("pages/7_Admin_Dashboard.py")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # SUPPORT
    # -------------------------------------------------------

    st.sidebar.caption("📧 manandkumar@gmail.com")