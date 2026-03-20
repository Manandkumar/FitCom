# -------------------------------------------------------
# FitCom - Supabase Database Configuration (FIXED)
# -------------------------------------------------------

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------------------------
# DATABASE URL
# -------------------------------------------------------

DATABASE_URL = st.secrets["DATABASE_URL"]

# -------------------------------------------------------
# ENGINE
# -------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# -------------------------------------------------------
# SESSION
# -------------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -------------------------------------------------------
# BASE
# -------------------------------------------------------

Base = declarative_base()