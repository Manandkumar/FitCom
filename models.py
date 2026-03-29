# -------------------------------------------------------
# FitCom - Database Models (SUPABASE READY)
# Author: Anand Kumar
# -------------------------------------------------------

from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base


# =======================================================
# REPORT TABLE
# =======================================================

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    # Multi-user
    UserId = Column(String, index=True)

    # User Info
    Name = Column(String, index=True, nullable=False)
    Gender = Column(String)
    Date = Column(String, index=True)
    Photo = Column(String)

    # Metrics
    Age = Column(Integer)
    Height = Column(Float)
    Weight = Column(Float)

    BMI = Column(Float)
    BodyFat = Column(Float)
    FatMass = Column(Float)
    FatFreeBodyWeight = Column(Float)

    MuscleMass = Column(Float)
    MuscleRate = Column(Float)
    SkeletalMuscle = Column(Float)

    BoneMass = Column(Float)
    SubcutaneousFat = Column(Float)

    BodyWater = Column(Float)
    WaterWeight = Column(Float)

    ProteinMass = Column(Float)
    ProteinRate = Column(Float)

    VisceralFat = Column(Float)
    BMR = Column(Float)
    BodyAge = Column(Integer)
    WHR = Column(Float)

    IdealBodyWeight = Column(Float)

    IsDeleted = Column(Boolean, default=False, index=True)


# =======================================================
# HIIT SESSION TABLE
# =======================================================

class HIITSession(Base):
    __tablename__ = "hiit_sessions"

    id = Column(Integer, primary_key=True, index=True)

    UserId = Column(String, index=True)

    Name = Column(String, index=True)
    Date = Column(String, index=True)

    Workout = Column(String)
    Duration = Column(Integer)

    Calories = Column(Integer)
    HeartRate = Column(Integer)

    Notes = Column(String)

    IsDeleted = Column(Boolean, default=False, index=True)