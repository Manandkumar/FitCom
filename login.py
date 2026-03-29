# ============================================================
# FitCom - Login (Production Ready)
# Author: Anand Kumar
# ============================================================

import streamlit as st

# Safe import (VERY IMPORTANT)
try:
    from storage.supabase_storage import sign_in, sign_up
    AUTH_AVAILABLE = True
except Exception as e:
    AUTH_AVAILABLE = False
    AUTH_ERROR = str(e)


def login():
    st.title("🔐 FitCom Login")

    # 🚨 If auth system failed
    if not AUTH_AVAILABLE:
        st.error(f"Auth system not available: {AUTH_ERROR}")
        st.stop()

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # ========================================================
    # 🔹 LOGIN TAB
    # ========================================================
    with tab1:

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", use_container_width=True):

            # Basic validation
            if not email or not password:
                st.warning("Please enter email and password")
                return

            try:
                res = sign_in(email, password)

                if res and res.user:
                    # ✅ Store session
                    st.session_state["user"] = res.user.email
                    st.session_state["access_token"] = res.session.access_token

                    st.success("Login successful ✅")
                    st.rerun()

                else:
                    st.error("Invalid email or password")

            except Exception as e:
                st.error(f"Login failed: {e}")

    # ========================================================
    # 🔹 SIGNUP TAB
    # ========================================================
    with tab2:

        new_email = st.text_input("New Email", key="signup_email")
        new_password = st.text_input("New Password", type="password", key="signup_password")

        if st.button("Create Account", use_container_width=True):

            # Basic validation
            if not new_email or not new_password:
                st.warning("Please enter email and password")
                return

            if len(new_password) < 6:
                st.warning("Password must be at least 6 characters")
                return

            try:
                res = sign_up(new_email, new_password)

                if res and res.user:
                    st.success("Account created 🎉 Please login.")
                else:
                    st.error("Signup failed. Check Supabase settings.")

            except Exception as e:
                st.error(f"Signup failed: {e}")