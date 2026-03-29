import streamlit as st

def login():

    st.title("🔐 FitCom Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        # Simple demo auth (replace later with real auth)
        if username and password:
            st.session_state["user"] = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")