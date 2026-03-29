# ============================================================
# FitCom - Sidebar (User Aware)
# Author: Anand Kumar
# ============================================================

import streamlit as st
from storage.supabase_storage import sign_out


def render_sidebar():

    with st.sidebar:

        user = st.session_state.get("user")

        st.markdown("## 🏋️ FitCom")

        if user:
            st.markdown(f"👤 **{user}**")

            st.markdown("---")

            # ✅ MAIN USER VIEW
            st.page_link("Dashboard.py", label="🏠 My Dashboard")

            st.page_link(
                "pages/9_Member_Dashboard.py",
                label="📊 My Progress"
            )

            # Optional features
            st.page_link("pages/2_Progress.py", label="📈 Progress")
            st.page_link("pages/4_AI_Coach.py", label="🤖 AI Coach")

            st.markdown("---")

            # ✅ ADD MEMBER (OPTIONAL – YOU DECIDE)
            st.page_link(
                "pages/1_Add_NewMember.py",
                label="➕ Add Member"
            )

            st.markdown("---")

            # LOGOUT
            if st.button("🚪 Logout"):
                sign_out()
                st.session_state.clear()
                st.rerun()

        else:
            st.warning("Please login")