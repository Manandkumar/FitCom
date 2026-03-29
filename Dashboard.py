# ============================================================
# FitCom - Dashboard (ENTRY POINT)
# Author: Anand Kumar
# ============================================================

# ------------------------------------------------------------
# ROOT PATH FIX (APPLIES TO WHOLE APP)
# ------------------------------------------------------------
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add project root so modules like database.py are discoverable
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ------------------------------------------------------------
# NORMAL IMPORTS (NOW WILL WORK)
# ------------------------------------------------------------
import streamlit as st

from login import login
from storage import load_reports
from sidebar import render_sidebar

# ------------------------------------------------------------
# LOGIN PROTECTION
# ------------------------------------------------------------
if "user" not in st.session_state:
    login()
    st.stop()

# ------------------------------------------------------------
# UI
# ------------------------------------------------------------
st.title("📊 FitCom Dashboard")

render_sidebar()

data = load_reports()

st.write("Loaded Data:", data)