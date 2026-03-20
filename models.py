# -------------------------------------------------------
# FitCom - Database Models
# -------------------------------------------------------

from sqlalchemy import Column, Integer, String, Float
from database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    Name = Column(String)
    Gender = Column(String)
    Date = Column(String)
    Photo = Column(String)

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