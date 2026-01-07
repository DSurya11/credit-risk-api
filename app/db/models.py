from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    no_of_dependents = Column(Integer, nullable=False)
    income_annum = Column(Float, nullable=False)
    loan_amount = Column(Float, nullable=False)
    loan_term = Column(Integer, nullable=False)
    cibil_score = Column(Integer, nullable=False)
    bank_asset_value = Column(Float, nullable=False)

    risk_probability = Column(Float, nullable=False)
    decision = Column(String(20), nullable=False)
    threshold_used = Column(Float, nullable=False)
