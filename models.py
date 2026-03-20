# -------------------------------------------------------
# FitCom - Database Models (FINAL PRODUCTION VERSION)
# -------------------------------------------------------

from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base


# =======================================================
# REPORT TABLE
# =======================================================

class Report(Base):
    __tablename__ = "reports"

    # ---------------------------------------------------
    # PRIMARY KEY
    # ---------------------------------------------------
    id = Column(Integer, primary_key=True, index=True)

    # ---------------------------------------------------
    # USER INFO
    # ---------------------------------------------------
    Name = Column(String, index=True)
    Gender = Column(String)
    Date = Column(String, index=True)
    Photo = Column(String)

    # ---------------------------------------------------
    # BASIC METRICS
    # ---------------------------------------------------
    Age = Column(Integer)
    Height = Column(Float)
    Weight = Column(Float)

    # ---------------------------------------------------
    # BODY COMPOSITION
    # ---------------------------------------------------
    BMI = Column(Float)
    BodyFat = Column(Float)
    FatMass = Column(Float)
    FatFreeBodyWeight = Column(Float)

    # ---------------------------------------------------
    # MUSCLE
    # ---------------------------------------------------
    MuscleMass = Column(Float)
    MuscleRate = Column(Float)
    SkeletalMuscle = Column(Float)

    # ---------------------------------------------------
    # BODY DETAILS
    # ---------------------------------------------------
    BoneMass = Column(Float)
    SubcutaneousFat = Column(Float)

    # ---------------------------------------------------
    # HYDRATION
    # ---------------------------------------------------
    BodyWater = Column(Float)
    WaterWeight = Column(Float)

    # ---------------------------------------------------
    # PROTEIN
    # ---------------------------------------------------
    ProteinMass = Column(Float)
    ProteinRate = Column(Float)

    # ---------------------------------------------------
    # HEALTH METRICS
    # ---------------------------------------------------
    VisceralFat = Column(Float)
    BMR = Column(Float)
    BodyAge = Column(Integer)
    WHR = Column(Float)

    # ---------------------------------------------------
    # TARGET
    # ---------------------------------------------------
    IdealBodyWeight = Column(Float)

    # ---------------------------------------------------
    # SOFT DELETE
    # ---------------------------------------------------
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

    # ---------------------------------------------------
    # SOFT DELETE (CONSISTENT TYPE)
    # ---------------------------------------------------
    IsDeleted = Column(Boolean, default=False, nullable=False, index=True)