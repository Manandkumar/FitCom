# ============================================================
# FitCom - Login Module
# Author: Anand Kumar
# ============================================================

import streamlit as st


def login():
    """
    Simple session-based login.
    (Can be upgraded later to Supabase Auth)
    """

    st.title("🔐 FitCom Login")

    st.markdown("### Enter your credentials")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):

        # Basic validation (placeholder auth)
        if username and password:
            st.session_state["user"] = username
            st.success(f"Welcome {username} 👋")
            st.rerun()
        else:
            st.error("Please enter username and password")