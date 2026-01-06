import joblib
import pandas as pd

bundle = joblib.load("credit_risk_artifacts.pkl")

model = bundle["model"]
scaler = bundle["scaler"]
features = bundle["features"]

def predict_risk(data):
    row = {
        "no_of_dependents": data.no_of_dependents,
        "income_annum": data.income_annum,
        "loan_amount": data.loan_amount,
        "loan_term": data.loan_term,
        "cibil_score": data.cibil_score,
        "bank_asset_value": data.bank_asset_value
    }

    df = pd.DataFrame([row])[features]
    x_scaled = scaler.transform(df)
    prob = model.predict_proba(x_scaled)[0][1]

    return float(prob)
