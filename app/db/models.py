from sqlalchemy import Column, Integer, Float, String
from app.db.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    no_of_dependents = Column(Integer)
    income_annum = Column(Float)
    loan_amount = Column(Float)
    loan_term = Column(Integer)
    cibil_score = Column(Integer)
    bank_asset_value = Column(Float)
    risk_probability = Column(Float)
    decision = Column(String(20))
    threshold_used = Column(Float)
