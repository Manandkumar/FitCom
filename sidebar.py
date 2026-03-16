# ============================================================
# Syntra AI Sidebar
# Author: Anand Kumar
# ============================================================

import streamlit as st

def render_sidebar():

    # Sidebar styling
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
         # Contact section
            st.sidebar.markdown("### Need Help?")
            st.sidebar.markdown(
            """
            **Anand Kumar**  
            📧 anand@example.com  
            """
    )


    # Logo at the top
    # st.sidebar.image("logo.png", width=160)

    # App title
    # st.sidebar.title("Syntra AI")

    # Divider
    # st.sidebar.markdown("---")