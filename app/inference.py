import joblib
import pandas as pd
import sklearn
import logging

logger = logging.getLogger(__name__)

bundle = joblib.load("credit_risk_artifacts.pkl", mmap_mode=None)

model = bundle["model"]
scaler = bundle["scaler"]
features = bundle["features"]


def _patch_monotonic_cst(estimator):
    """Recursively set monotonic_cst=None on all tree-based estimators.

    Required when a model trained with scikit-learn 1.3.x is loaded
    in scikit-learn >= 1.6 where DecisionTreeClassifier expects the
    monotonic_cst attribute to exist.
    """
    if not hasattr(estimator, "monotonic_cst"):
        estimator.monotonic_cst = None
    if hasattr(estimator, "estimators_"):
        for sub in estimator.estimators_:
            _patch_monotonic_cst(sub)


if sklearn.__version__ != "1.3.2":
    logger.info(
        "Patching model for scikit-learn %s compatibility", sklearn.__version__
    )
    _patch_monotonic_cst(model)


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