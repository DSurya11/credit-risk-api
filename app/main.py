from fastapi import FastAPI
from app.schemas import loaninput, predictionresponse
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.crud import create_prediction_record

from app.inference import predict_risk
from app.config import approval_threshold

from typing import List
from app.schemas import predictionout
from app.db.crud import get_prediction_records

from app.db.database import engine, Base
import app.db.models


app = FastAPI()



@app.get("/")
def root():
    return {"message": "credit risk service running"}

@app.get("/predictions", response_model=List[predictionout])
def get_predictions(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return get_prediction_records(db=db, limit=limit, offset=offset)


@app.post("/predict", response_model=predictionresponse)
def predict(
    data: loaninput,
    db: Session = Depends(get_db)
):
    risk_probability = predict_risk(data)

    decision = "approved" if risk_probability >= approval_threshold else "rejected"

    create_prediction_record(
        db=db,
        no_of_dependents=data.no_of_dependents,
        income_annum=data.income_annum,
        loan_amount=data.loan_amount,
        loan_term=data.loan_term,
        cibil_score=data.cibil_score,
        bank_asset_value=data.bank_asset_value,
        risk_probability=risk_probability,
        decision=decision,
        threshold_used=approval_threshold
    )

    return predictionresponse(
        risk_probability=risk_probability,
        decision=decision
    )

