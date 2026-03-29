# -------------------------------------------------------
# FitCom - Database Models
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
    Name = Column(String, index=True)
    Gender = Column(String)
    Date = Column(String, index=True)
    Photo = Column(String)

    # Basic Metrics
    Age = Column(Integer)
    Height = Column(Float)
    Weight = Column(Float)

    # Body Composition
    BMI = Column(Float)
    BodyFat = Column(Float)
    FatMass = Column(Float)
    FatFreeBodyWeight = Column(Float)

    # Muscle
    MuscleMass = Column(Float)
    MuscleRate = Column(Float)
    SkeletalMuscle = Column(Float)

    # Body Details
    BoneMass = Column(Float)
    SubcutaneousFat = Column(Float)

    # Hydration
    BodyWater = Column(Float)
    WaterWeight = Column(Float)

    # Protein
    ProteinMass = Column(Float)
    ProteinRate = Column(Float)

    # Health Metrics
    VisceralFat = Column(Float)
    BMR = Column(Float)
    BodyAge = Column(Integer)
    WHR = Column(Float)

    # Target
    IdealBodyWeight = Column(Float)

    # Soft Delete
    IsDeleted = Column(Boolean, default=False, nullable=False, index=True)


# =======================================================
# HIIT WORKOUT TABLE
# =======================================================

class HIITSession(Base):
    __tablename__ = "hiit_sessions"

    id = Column(Integer, primary_key=True, index=True)

    Name = Column(String, index=True)
    Date = Column(String, index=True)

    Workout = Column(String)
    Duration = Column(Integer)

    Calories = Column(Integer)
    HeartRate = Column(Integer)

    Notes = Column(String)

    # Soft Delete
    IsDeleted = Column(Boolean, default=False, nullable=False, index=True)


# -------------------------------------------------------
# CREATE TABLES (SAFE TO RUN MULTIPLE TIMES)
# -------------------------------------------------------

from database import engine

Base.metadata.create_all(bind=engine)