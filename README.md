# Credit Risk Prediction API

A **FastAPI-based backend service** that predicts loan approval risk using a trained machine learning model.
The system accepts applicant financial data, calculates the probability of default, and returns an **approval or rejection decision** while storing predictions in a database.

This project demonstrates how to integrate **machine learning inference with a production-style backend system** using FastAPI, SQLAlchemy, and Docker.

---

## Live API

- **Base URL**: https://credit-risk-api-wpam.onrender.com
- **Swagger Docs**: https://credit-risk-api-wpam.onrender.com/docs

---

## Features

- Machine learning–based credit risk prediction
- REST API built with **FastAPI**
- **SQLAlchemy database integration** for storing prediction records
- Probability-based **loan approval decision system**
- Docker support for containerized deployment
- Retrieval of previous prediction records through API
- Deployed on **Render** with PostgreSQL

---

## Tech Stack

| Layer            | Technology                              |
| ---------------- | --------------------------------------- |
| Backend          | Python, FastAPI                         |
| Machine Learning | Scikit-learn (serialized model artifact) |
| Database         | PostgreSQL (Render), SQLAlchemy ORM     |
| Deployment       | Docker, Render (Cloud)                  |

---

## Project Structure

```
credit-risk-api
│
├── app
│   ├── main.py            # FastAPI application and endpoints
│   ├── config.py           # Configuration (approval threshold)
│   ├── inference.py        # ML model loading and prediction
│   ├── schemas.py          # Pydantic request/response models
│   │
│   └── db
│       ├── database.py     # Database connection and session
│       ├── models.py       # SQLAlchemy table definitions
│       ├── crud.py         # Database operations
│
├── credit_risk_artifacts.pkl   # Trained ML model bundle
├── create_tables.py
├── requirements.txt
├── Dockerfile
└── .env.example
```

---

## System Workflow

```
Client Request
      ↓
FastAPI Backend (validates input)
      ↓
ML Model (predicts risk probability)
      ↓
Decision Engine (approved / rejected)
      ↓
PostgreSQL (stores prediction record)
      ↓
JSON Response → Client
```

1. Client sends loan applicant details to the `/predict` endpoint.
2. FastAPI backend receives and validates the request.
3. The trained ML model loads from `credit_risk_artifacts.pkl`.
4. The model calculates **risk probability**.
5. Backend compares probability with a configured **approval threshold**.
6. Decision is generated: `approved` or `rejected`.
7. Prediction data is stored in the database.
8. Response is returned to the client.

---

## API Endpoints

### Health Check

```
GET /
```

Response:

```json
{
  "message": "credit risk service running"
}
```

---

### Predict Credit Risk

```
POST /predict
```

Request:

```json
{
  "no_of_dependents": 2,
  "income_annum": 450000,
  "loan_amount": 120000,
  "loan_term": 12,
  "cibil_score": 720,
  "bank_asset_value": 300000
}
```

Response:

```json
{
  "risk_probability": 0.27,
  "decision": "approved"
}
```

---

### Get Previous Predictions

```
GET /predictions?limit=10&offset=0
```

| Parameter | Description                 |
| --------- | --------------------------- |
| limit     | Number of records to return |
| offset    | Pagination offset           |

---

## Live Example

```bash
curl -X POST https://credit-risk-api-wpam.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "no_of_dependents": 2,
    "income_annum": 450000,
    "loan_amount": 120000,
    "loan_term": 12,
    "cibil_score": 720,
    "bank_asset_value": 300000
  }'
```

```json
{
  "risk_probability": 0.27,
  "decision": "approved"
}
```

---

## Running Locally

```bash
# Clone the repository
git clone https://github.com/DSurya11/credit-risk-api.git
cd credit-risk-api

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your database credentials

# Run the API
uvicorn app.main:app --reload
```

Server: `http://127.0.0.1:8000`
Swagger docs: `http://127.0.0.1:8000/docs`

---

## Docker Setup

```bash
# Build
docker build -t credit-risk-api .

# Run
docker run -p 8000:8000 credit-risk-api
```

---

## Future Improvements

- Authentication and authorization
- Model monitoring and retraining pipeline
- API rate limiting
- Feature store for model inputs
- Logging and observability

---

## Author

**Surya**
GitHub: [DSurya11](https://github.com/DSurya11)
