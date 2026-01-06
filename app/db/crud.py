from sqlalchemy.orm import Session
from .models import predictionrequest

def create_prediction_record(
    db: Session,
    no_of_dependents: int,
    income_annum: float,
    loan_amount: float,
    loan_term: int,
    cibil_score: int,
    bank_asset_value: float,
    risk_probability: float,
    decision: str,
    threshold_used: float
):
    record = predictionrequest(
        no_of_dependents=no_of_dependents,
        income_annum=income_annum,
        loan_amount=loan_amount,
        loan_term=loan_term,
        cibil_score=cibil_score,
        bank_asset_value=bank_asset_value,
        risk_probability=risk_probability,
        decision=decision,
        threshold_used=threshold_used
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_prediction_records(db: Session, limit: int = 10, offset: int = 0):
    return (
        db.query(predictionrequest)
        .order_by(predictionrequest.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
