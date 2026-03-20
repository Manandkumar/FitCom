# -------------------------------------------------------
# FitCom - Supabase Database Configuration (FINAL)
# -------------------------------------------------------

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------------------------
# LOAD DATABASE URL FROM STREAMLIT SECRETS
# -------------------------------------------------------

DATABASE_URL = st.secrets["DATABASE_URL"]

# -------------------------------------------------------
# ENGINE (POSTGRESQL)
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
# BASE MODEL
# -------------------------------------------------------

Base = declarative_base()

# -------------------------------------------------------
# AUTO CREATE TABLES
# -------------------------------------------------------

from models import Base
Base.metadata.create_all(bind=engine)