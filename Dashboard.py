# ============================================================
# FitCom - Dashboard (ENTRY POINT)
# Author: Anand Kumar
# ============================================================

# ------------------------------------------------------------
# ROOT PATH FIX (CRITICAL – DO THIS ONLY HERE)
# ------------------------------------------------------------
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ------------------------------------------------------------
# NORMAL IMPORTS (NOW THESE WILL WORK)
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
# YOUR EXISTING DASHBOARD CODE BELOW
# (keep everything else as is)
# ------------------------------------------------------------

st.title("📊 FitCom Dashboard")

render_sidebar()

data = load_reports()

st.write("Loaded Data:", data)