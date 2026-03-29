# -------------------------------------------------------
# FitCom - Database Models (SUPABASE READY)
# -------------------------------------------------------

from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base


# =======================================================
# REPORT TABLE
# =======================================================

class Report(Base):
    __tablename__ = "reports"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # User Info
    Name = Column(String, index=True, nullable=False)
    Gender = Column(String, nullable=True)
    Date = Column(String, index=True, nullable=False)
    Photo = Column(String, nullable=True)

    # Basic Metrics
    Age = Column(Integer, nullable=True)
    Height = Column(Float, nullable=True)
    Weight = Column(Float, nullable=True)

    # Body Composition
    BMI = Column(Float, nullable=True)
    BodyFat = Column(Float, nullable=True)
    FatMass = Column(Float, nullable=True)
    FatFreeBodyWeight = Column(Float, nullable=True)

    # Muscle
    MuscleMass = Column(Float, nullable=True)
    MuscleRate = Column(Float, nullable=True)
    SkeletalMuscle = Column(Float, nullable=True)

    # Body Details
    BoneMass = Column(Float, nullable=True)
    SubcutaneousFat = Column(Float, nullable=True)

    # Hydration
    BodyWater = Column(Float, nullable=True)
    WaterWeight = Column(Float, nullable=True)

    # Protein
    ProteinMass = Column(Float, nullable=True)
    ProteinRate = Column(Float, nullable=True)

    # Health Metrics
    VisceralFat = Column(Float, nullable=True)
    BMR = Column(Float, nullable=True)
    BodyAge = Column(Integer, nullable=True)
    WHR = Column(Float, nullable=True)

    # Target
    IdealBodyWeight = Column(Float, nullable=True)

    # Soft Delete
    IsDeleted = Column(Boolean, default=False, nullable=False, index=True)


# =======================================================
# HIIT WORKOUT TABLE
# =======================================================

class HIITSession(Base):
    __tablename__ = "hiit_sessions"

    id = Column(Integer, primary_key=True, index=True)

    Name = Column(String, index=True, nullable=False)
    Date = Column(String, index=True, nullable=False)

    Workout = Column(String, nullable=True)
    Duration = Column(Integer, nullable=True)

    Calories = Column(Integer, nullable=True)
    HeartRate = Column(Integer, nullable=True)

    Notes = Column(String, nullable=True)

    # Soft Delete
    IsDeleted = Column(Boolean, default=False, nullable=False, index=True)


# -------------------------------------------------------
# CREATE TABLES (SAFE TO RUN MULTIPLE TIMES)
# -------------------------------------------------------

from database import engine

def create_tables():
    """
    Explicit table creation function.
    Called once when app starts.
    """
    Base.metadata.create_all(bind=engine)


# Call once on import
create_tables()