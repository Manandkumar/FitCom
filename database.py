# ============================================================
# FitCom - Database Configuration
# Author: Anand Kumar
# ============================================================

import os
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# ============================================================
# DATABASE URL
# ============================================================

def get_database_url():
    """
    Load DB URL safely
    """

    try:
        return st.secrets["DATABASE_URL"]
    except Exception:
        return os.getenv("DATABASE_URL", "sqlite:///./fitcom.db")


DATABASE_URL = get_database_url()


# ============================================================
# ENGINE
# ============================================================

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=False
)


# ============================================================
# SESSION
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ============================================================
# BASE
# ============================================================

Base = declarative_base()