# Credit Risk Prediction API

A **FastAPI-based backend service** that predicts loan approval risk using a trained machine learning model.
The system accepts applicant financial data, calculates the probability of default, and returns an **approval or rejection decision** while storing predictions in a database.

This project demonstrates how to integrate **machine learning inference with a production-style backend system** using FastAPI, SQLAlchemy, and Docker.

---

# Features

* Machine learning–based credit risk prediction
* REST API built with **FastAPI**
* **SQLAlchemy database integration** for storing prediction records
* Probability-based **loan approval decision system**
* Docker support for containerized deployment
* Retrieval of previous prediction records through API

---

# Tech Stack

Backend

* Python
* FastAPI

Machine Learning

* Scikit-learn model (stored as serialized artifact)

Database

* SQLAlchemy ORM
* Relational database (MySQL/PostgreSQL compatible)

Deployment

* Docker

---

# Project Structure

```
credit-risk-api
│
├── app
│   ├── main.py
│   ├── config.py
│   ├── inference.py
│   ├── schemas.py
│   │
│   └── db
│       ├── database.py
│       ├── models.py
│       ├── crud.py
│
├── credit_risk_artifacts.pkl
├── create_tables.py
├── requirements.txt
├── Dockerfile
└── project.ipynb
```

---

# System Workflow

1. Client sends loan applicant details to the `/predict` endpoint.
2. FastAPI backend receives and validates the request.
3. The trained ML model loads from `credit_risk_artifacts.pkl`.
4. The model calculates **risk probability**.
5. Backend compares probability with a configured **approval threshold**.
6. Decision is generated:

   * `approved`
   * `rejected`
7. Prediction data is stored in the database.
8. Response is returned to the client.

---

# API Endpoints

## Health Check

```
GET /
```

Response

```json
{
  "message": "credit risk service running"
}
```

---

## Predict Credit Risk

```
POST /predict
```

Request Example

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

Response Example

```json
{
  "risk_probability": 0.27,
  "decision": "approved"
}
```

---

## Get Previous Predictions

```
GET /predictions
```

Query Parameters

| Parameter | Description                 |
| --------- | --------------------------- |
| limit     | Number of records to return |
| offset    | Pagination offset           |

Example

```
GET /predictions?limit=10&offset=0
```

---

# Running the Project Locally

Clone the repository

```
git clone https://github.com/DSurya11/credit-risk-api.git
cd credit-risk-api
```

Create virtual environment

```
python -m venv venv
```

Activate environment

Windows

```
venv\Scripts\activate
```

Install dependencies

```
pip install -r requirements.txt
```

Run the API

```
uvicorn app.main:app --reload
```

Server runs at

```
http://127.0.0.1:8000
```

Swagger API documentation

```
http://127.0.0.1:8000/docs
```

---

# Docker Setup

Build Docker image

```
docker build -t credit-risk-api .
```

Run container

```
docker run -p 8000:8000 credit-risk-api
```

---

# Future Improvements

* Authentication and authorization
* Model monitoring and retraining pipeline
* API rate limiting
* Cloud deployment
* Feature store for model inputs
* Logging and observability

---

# Author

Surya
GitHub: https://github.com/DSurya11
