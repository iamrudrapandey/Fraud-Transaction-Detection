from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime

from database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    Time = Column(Float)
    Amount = Column(Float)

    V1 = Column(Float)
    V2 = Column(Float)
    V3 = Column(Float)
    V4 = Column(Float)
    V5 = Column(Float)
    V6 = Column(Float)
    V7 = Column(Float)
    V8 = Column(Float)
    V9 = Column(Float)
    V10 = Column(Float)
    V11 = Column(Float)
    V12 = Column(Float)
    V13 = Column(Float)
    V14 = Column(Float)
    V15 = Column(Float)
    V16 = Column(Float)
    V17 = Column(Float)
    V18 = Column(Float)
    V19 = Column(Float)
    V20 = Column(Float)
    V21 = Column(Float)
    V22 = Column(Float)
    V23 = Column(Float)
    V24 = Column(Float)
    V25 = Column(Float)
    V26 = Column(Float)
    V27 = Column(Float)
    V28 = Column(Float)

    prediction = Column(String)
    fraud_probability = Column(Float)
    risk_level = Column(String)
    threshold = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    