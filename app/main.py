import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import loaninput, predictionresponse, predictionout
from app.db.database import get_db, create_tables
from app.db.crud import create_prediction_record, get_prediction_records, delete_prediction_record
from app.inference import predict_risk
from app.config import approval_threshold

# Ensure models are imported so Base knows about them
import app.db.models  # noqa: F401

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run on startup: create database tables if they don't exist."""
    logger.info("Creating database tables if they do not exist...")
    try:
        create_tables()
        logger.info("Database tables ready.")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}", exc_info=True)
        # Don't block startup — endpoints will return clear errors if DB is down
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "credit risk service running"}


@app.get("/predictions", response_model=List[predictionout])
def get_predictions(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    try:
        return get_prediction_records(db=db, limit=limit, offset=offset)
    except Exception as e:
        logger.error(f"Error fetching predictions: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/predict", response_model=predictionresponse)
def predict(
    data: loaninput,
    db: Session = Depends(get_db)
):
    # Step 1: Run ML inference (this must succeed)
    try:
        risk_probability = predict_risk(data)
    except Exception as e:
        logger.error(f"ML inference failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Model error: {str(e)}")

    decision = "approved" if risk_probability >= approval_threshold else "rejected"

    # Step 2: Save to database (best-effort — don't fail if DB is down)
    try:
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
    except Exception as e:
        logger.warning(f"Could not save prediction to database: {e}")

    return predictionresponse(
        risk_probability=risk_probability,
        decision=decision
    )


@app.delete("/predictions/{prediction_id}")
def delete_prediction(
    prediction_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_prediction_record(db=db, prediction_id=prediction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return {"message": f"Prediction {prediction_id} deleted"}
