# -------------------------------------------------------
# FitCom - Database Configuration
# -------------------------------------------------------

import os
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------------------------
# DATABASE URL (SAFE LOADING)
# -------------------------------------------------------

def get_database_url():
    """
    Load database URL safely.
    Priority:
    1. Streamlit secrets
    2. Environment variable
    3. Local SQLite fallback
    """
    try:
        return st.secrets["DATABASE_URL"]
    except Exception:
        return os.getenv("DATABASE_URL", "sqlite:///./fitcom.db")


DATABASE_URL = get_database_url()

# -------------------------------------------------------
# ENGINE
# -------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # avoids stale connections
    echo=False            # set True only for debugging
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