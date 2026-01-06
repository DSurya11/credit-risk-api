from pydantic import BaseModel
from datetime import datetime

class predictionout(BaseModel):
    id: int
    created_at: datetime

    no_of_dependents: int
    income_annum: float
    loan_amount: float
    loan_term: int
    cibil_score: int
    bank_asset_value: float

    risk_probability: float
    decision: str
    threshold_used: float

    class Config:
        orm_mode = True


class loaninput(BaseModel):
    no_of_dependents: int
    income_annum: float
    loan_amount: float
    loan_term: int
    cibil_score: int
    bank_asset_value: float

class predictionresponse(BaseModel):
    risk_probability: float
    decision: str