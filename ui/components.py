import streamlit as st

def page_header(title, subtitle=""):
    st.markdown(f"<h2>{title}</h2>", unsafe_allow_html=True)
    if subtitle:
        st.caption(subtitle)

def section(title):
    st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)

def card(content):
    st.markdown(f"""
    <div style='padding:15px;border-radius:12px;
    background:#ffffff;
    box-shadow:0 4px 10px rgba(0,0,0,0.05);
    margin-bottom:10px;'>
    {content}
    </div>
    """, unsafe_allow_html=True)