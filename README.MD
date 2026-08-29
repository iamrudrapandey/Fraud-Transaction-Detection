# 🛡️ FraudGuard AI

### AI-Powered Credit Card Fraud Detection System

FraudGuard AI is a machine-learning-based web application that analyzes credit card transactions and predicts whether a transaction is **legitimate or potentially fraudulent**.

The system combines an **XGBoost classifier**, **SMOTE class balancing**, **FastAPI**, **React**, and **SQLite** to provide real-time fraud detection with prediction history and analytics.

---

## 🚀 Features

* 🤖 AI-powered fraud prediction
* 📊 XGBoost classification model
* ⚖️ SMOTE for handling class imbalance
* 🔍 Real-time transaction analysis
* 📈 Fraud probability score
* 🚦 Risk-level classification
* 💾 SQLite prediction history
* 📊 Fraud vs legitimate analytics
* 🩺 API and database health monitoring
* ⚡ React + Vite frontend
* 🚀 FastAPI backend
* ✅ Input validation and error handling
* 📱 Responsive dashboard interface

---

## 🧠 Machine Learning Model

FraudGuard AI uses an **XGBoost Classifier** trained on credit-card transaction data.

### Model Performance

| Metric    |  Score |
| --------- | -----: |
| Precision | 92.50% |
| Recall    | 77.89% |
| F1 Score  | 84.57% |

The system uses **SMOTE (Synthetic Minority Over-sampling Technique)** to address the highly imbalanced nature of fraud datasets.

The optimized decision threshold used by the system is:

```text
0.305818
```

---

## 🏗️ Technology Stack

### Frontend

* React
* Vite
* Axios
* Recharts
* CSS

### Backend

* Python
* FastAPI
* Pydantic
* SQLite
* Uvicorn

### Machine Learning

* XGBoost
* Scikit-learn
* Pandas
* NumPy
* SMOTE

---

## 📂 Project Structure

```text
FraudGuard/
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   └── main.py
│
├── src/
│   └── predict.py
│
├── models/
│   └── model files
│
├── fraudguard.db
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd FraudGuard
```

---

## 2. Create Python Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

If you don't have `requirements.txt`, install the required packages:

```bash
pip install fastapi uvicorn pandas numpy scikit-learn xgboost imbalanced-learn pydantic
```

---

# 🖥️ Run the Backend

Navigate to the backend directory:

```bash
cd backend
```

Start FastAPI:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The backend will run at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🌐 Run the Frontend

Open another terminal.

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# 🔄 How the System Works

```text
User enters transaction
        ↓
React Frontend
        ↓
FastAPI Backend
        ↓
Input Validation
        ↓
XGBoost ML Model
        ↓
Fraud Probability
        ↓
Risk Classification
        ↓
SQLite Database
        ↓
Result displayed on Dashboard
```

---

# 🔌 API Endpoints

| Method | Endpoint   | Description                |
| ------ | ---------- | -------------------------- |
| GET    | `/`        | API information            |
| GET    | `/health`  | API/database health check  |
| POST   | `/predict` | Analyze transaction        |
| GET    | `/history` | Get prediction history     |
| GET    | `/stats`   | Get transaction statistics |
| DELETE | `/history` | Clear prediction history   |

---

# 🔍 Transaction Prediction

The `/predict` endpoint accepts transaction features including:

```text
Time
V1 - V28
Amount
```

The API returns information such as:

```json
{
  "prediction": "LEGITIMATE",
  "fraud_probability_percent": 2.45,
  "risk_level": "LOW",
  "threshold": 0.305818,
  "saved_to_database": true
}
```

---

# 📊 Dashboard

FraudGuard provides four main sections:

### Dashboard Overview

Displays:

* Total transactions
* Fraud detected
* Legitimate transactions
* Fraud rate
* Recent predictions
* Model performance

### Transaction Scanner

Allows users to:

* Enter transaction features
* Load demo transaction
* Analyze transactions
* View fraud probability
* View risk level

### Prediction History

Displays:

* Previous predictions
* Transaction amount
* Fraud probability
* Risk level
* Prediction time

### Model Performance

Displays:

* Precision
* Recall
* F1 Score
* Algorithm
* SMOTE configuration
* Decision threshold

---

# 🗄️ Database

FraudGuard uses **SQLite** to store prediction results.

The database stores:

* Transaction features
* Prediction
* Fraud probability
* Risk level
* Decision threshold
* Prediction timestamp

The database file is automatically created when the backend starts.

---

# 🛡️ Error Handling

The backend includes error handling for:

* Invalid transaction data
* Negative transaction amounts
* ML prediction failures
* Database errors
* API failures
* Connection problems

The frontend also displays appropriate error messages when the backend cannot be reached.

---

# 🔐 Security Notes

This project is designed for educational and demonstration purposes.

Do not use the model as the sole decision-maker for real financial transactions without additional security, validation, monitoring, and compliance controls.

---

# 📌 Future Improvements

Possible future improvements include:

* User authentication
* JWT-based authorization
* Cloud database
* Docker deployment
* Model retraining pipeline
* Advanced transaction analytics
* Confusion matrix visualization
* ROC-AUC visualization
* SHAP-based prediction explanations
* Cloud deployment
* Automated model monitoring

---

# 👨‍💻 Author

**Rudra**

AI Fraud Detection Project

---

## ⭐ Project Summary

FraudGuard AI demonstrates how machine learning can be integrated with a modern web application to create a real-time credit card fraud detection system.

**XGBoost + SMOTE + FastAPI + React + SQLite**
