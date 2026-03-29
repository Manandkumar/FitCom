from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    # ✅ NEW
    UserId = Column(String, index=True)

    Name = Column(String, index=True, nullable=False)
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

    IsDeleted = Column(Boolean, default=False)


class HIITSession(Base):
    __tablename__ = "hiit_sessions"

    id = Column(Integer, primary_key=True, index=True)

    # ✅ NEW
    UserId = Column(String, index=True)

    Name = Column(String)
    Date = Column(String)

    Workout = Column(String)
    Duration = Column(Integer)

    Calories = Column(Integer)
    HeartRate = Column(Integer)

    Notes = Column(String)

    IsDeleted = Column(Boolean, default=False)