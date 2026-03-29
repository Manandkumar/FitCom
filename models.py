# -------------------------------------------------------
# FitCom - Database Models (PRODUCTION READY)
# -------------------------------------------------------

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
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

    MuscleMass = Column(Float)
    VisceralFat = Column(Float)
    BMR = Column(Float) 

    # ✅ NEW (IMPORTANT)
    # HealthScore = Column(Float)

    IsDeleted = Column(Boolean, default=False, index=True)


# =======================================================
# HIIT SESSION TABLE (FIXED STRUCTURE)
# =======================================================

class HIITSession(Base):
    __tablename__ = "hiit_sessions"

    id = Column(Integer, primary_key=True, index=True)

    # Link to user
    UserId = Column(String, index=True)

    # Optional future relation
    ReportId = Column(Integer, nullable=True)

    Name = Column(String, index=True)
    Date = Column(String, index=True)

    SessionNo = Column(Integer)
    Duration = Column(Integer)

    # ✅ Structured fields (instead of string mess)
    RunningDistance = Column(Float)
    SledgePush = Column(Float)
    SledgePull = Column(Float)
    LungeWalk = Column(Float)
    FarmersCarry = Column(Float)

    BoxJump = Column(Integer)
    WallBall = Column(Integer)

    IsDeleted = Column(Boolean, default=False, index=True)