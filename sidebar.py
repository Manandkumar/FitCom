# ============================================================
# FitCom - Sidebar Navigation (SaaS + Auth Ready)
# Author: Anand Kumar
# ============================================================

import streamlit as st
import os

# ✅ NEW IMPORT (AUTH LOGOUT)
from storage.supabase_storage import sign_out



def render_sidebar():

    # -------------------------------------------------------
    # SIDEBAR STYLING
    # -------------------------------------------------------

    st.markdown("""
    <style>

    div[data-testid="stSidebarNav"] {
        display: none;
    }

    section[data-testid="stSidebar"] {
        width: 260px !important;
        min-width: 260px !important;
        max-width: 260px !important;
        background-color: #F7F9FB;
        border-right: 1px solid #E6EAF0;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    section[data-testid="stSidebar"] * {
        font-size: 14px;
        color: #2C2C2C;
    }

    .logo-box {
        padding: 10px 6px;
        margin-bottom: 10px;
        border-bottom: 1px solid #E6EAF0;
    }

    section[data-testid="stSidebar"] a {
        display: block;
        padding: 10px 12px;
        margin: 4px 0;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.15s ease;
    }

    section[data-testid="stSidebar"] a:hover {
        background: rgba(31,167,161,0.08);
        color: #1FA7A1 !important;
    }

    section[data-testid="stSidebar"] a[aria-current="page"] {
        background: #1FA7A1 !important;
        color: white !important;
        font-weight: 600;
        box-shadow: 0 2px 6px rgba(31,167,161,0.25);
    }

    hr {
        border: none;
        height: 1px;
        background: #E6EAF0;
        margin: 10px 0;
    }

    .sidebar-footer {
        font-size: 12px;
        color: #888;
        margin-top: 12px;
        text-align: center;
    }

    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------
    # SIDEBAR CONTENT
    # -------------------------------------------------------

    with st.sidebar:

        # ---------------- LOGO ----------------
        st.markdown("<div class='logo-box'>", unsafe_allow_html=True)

        if os.path.exists("logo.png"):
            st.image("logo.png", width="stretch")
        else:
            st.markdown("### 🏋️ FitCom")

        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- USER INFO ----------------
        user = st.session_state.get("user", "Guest")
        st.markdown(f"👤 **{user}**")

        st.markdown("---")

        # ---------------- NAVIGATION ----------------
        st.page_link("Dashboard.py", label="🏠 Dashboard")
        st.page_link("pages/1_Add_NewMember.py", label="➕ Add Member")
        st.page_link("pages/2_Progress.py", label="📊 Progress")
        st.page_link("pages/3_Leaderboard.py", label="🏆 Leaderboard")
        st.page_link("pages/4_AI_Coach.py", label="🤖 AI Coach")
        st.page_link("pages/5_Athlete_Comparison.py", label="⚖️ Comparison")
        st.page_link("pages/6_Edit_Report.py", label="✏️ Edit Report")
        st.page_link("pages/8_Weekly_Report.py", label="📅 Weekly Report")
        st.page_link("pages/7_Admin_Dashboard.py", label="⚙️ Admin")

        st.markdown("---")

        # ---------------- LOGOUT ----------------
        if st.button("🚪 Logout", use_container_width=True):
            sign_out()                     # Supabase logout
            st.session_state.clear()       # Clear session
            st.rerun()

        # ---------------- FOOTER ----------------
        st.markdown(
            "<div class='sidebar-footer'>📧 manandkumar@gmail.com</div>",
            unsafe_allow_html=True
        )