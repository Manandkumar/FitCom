# ============================================================
# FitCom - Login (Supabase Auth)
# Author: Anand Kumar
# ============================================================

import streamlit as st
from storage.supabase_storage import sign_in, sign_up


def login():

    st.title("🔐 FitCom Login")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # LOGIN
    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            res = sign_in(email, password)

            if res and res.user:
                st.session_state["user"] = res.user.email
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # SIGN UP
    with tab2:
        email = st.text_input("New Email")
        password = st.text_input("New Password", type="password")

        if st.button("Create Account", use_container_width=True):
            res = sign_up(email, password)

            if res:
                st.success("Account created. Please login.")
            else:
                st.error("Signup failed")