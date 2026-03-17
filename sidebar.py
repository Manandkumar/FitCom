# ============================================================
# FitCom - Clean Sidebar (Balanced Layout)
# ============================================================

import streamlit as st

def render_sidebar():

    # -------------------------------------------------------
    # SIDEBAR STYLE (WHITE + CLEAN)
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

    /* Center logo nicely */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }

    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------
    # LOGO (PROPER SIZE - NOT SHRUNK)
    # -------------------------------------------------------

    st.sidebar.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.sidebar.image("logo.png", use_column_width=True)  # auto scales nicely
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # ALL MENU ITEMS (NO DROPDOWN)
    # -------------------------------------------------------

    if st.sidebar.button("🏠 Dashboard"):
        st.switch_page("Dashboard.py")

    if st.sidebar.button("📊 Progress"):
        st.switch_page("pages/2_Progress.py")

    if st.sidebar.button("➕ Add Member / Report"):
        st.switch_page("pages/1_Add_NewMember.py")

    if st.sidebar.button("🏆 Leaderboard"):
        st.switch_page("pages/3_Leaderboard.py")

    if st.sidebar.button("🤖 AI Coach"):
        st.switch_page("pages/4_AI_Coach.py")

    if st.sidebar.button("⚖️ Athlete Comparison"):
        st.switch_page("pages/5_Athlete_Comparison.py")

    if st.sidebar.button("✏️ Edit Report"):
        st.switch_page("pages/6_Edit_Report.py")

    if st.sidebar.button("📅 Weekly Report"):
        st.switch_page("pages/8_Weekly_Report.py")

    if st.sidebar.button("⚙️ Admin Dashboard"):
        st.switch_page("pages/7_Admin_Dashboard.py")

    st.sidebar.markdown("---")

    # -------------------------------------------------------
    # SUPPORT
    # -------------------------------------------------------

    st.sidebar.caption("📧 manandkumar@gmail.com")