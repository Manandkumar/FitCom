# -------------------------------------------------------
# FitCom - Database Configuration (PRODUCTION READY)
# -------------------------------------------------------

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------------------------
# PATH SETUP
# -------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "fitcom.db")

print(f"📁 DB PATH: {DB_PATH}")

DATABASE_URL = f"sqlite:///{DB_PATH}"

# -------------------------------------------------------
# ENGINE
# -------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # 🔥 set True only for debugging SQL logs
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