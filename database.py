# -------------------------------------------------------
# FitCom - Database Configuration (SUPABASE ONLY)
# -------------------------------------------------------

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------------------------
# DATABASE URL (MANDATORY - NO FALLBACK)
# -------------------------------------------------------

def get_database_url():
    """
    Load DATABASE_URL strictly from Streamlit secrets.
    Fail immediately if not found.
    """
    if "DATABASE_URL" not in st.secrets:
        raise ValueError(
            "❌ DATABASE_URL not found in .streamlit/secrets.toml. "
            "Supabase connection is required."
        )
    
    return st.secrets["DATABASE_URL"]


DATABASE_URL = get_database_url()

# -------------------------------------------------------
# ENGINE
# -------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # Keeps connection alive
    echo=False            # Set True only for debugging
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