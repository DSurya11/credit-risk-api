from app.db.database import sessionlocal
from app.db.crud import create_prediction_record

db = sessionlocal()

record = create_prediction_record(
    db=db,
    no_of_dependents=2,
    income_annum=500000,
    loan_amount=200000,
    loan_term=12,
    cibil_score=750,
    bank_asset_value=100000,
    risk_probability=0.32,
    decision="approved",
    threshold_used=0.5
)

print("inserted id:", record.id)

db.close()
