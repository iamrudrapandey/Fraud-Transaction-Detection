# 🛡️ FraudGuard AI

### AI-Powered Credit Card Fraud Detection System

[![Live Frontend](https://img.shields.io/badge/Live%20Demo-Frontend-success?style=for-the-badge)](https://fraud-transaction-detection-kj8o.onrender.com)
[![API](https://img.shields.io/badge/API-Live-blue?style=for-the-badge)](https://fraudguard-api-wk9h.onrender.com)
[![API Docs](https://img.shields.io/badge/API-Docs-orange?style=for-the-badge)](https://fraudguard-api-wk9h.onrender.com/docs)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge)](https://github.com/iamrudrapandey/Fraud-Transaction-Detection)

FraudGuard AI is a full-stack machine-learning application that detects potentially fraudulent credit card transactions in real time.

The project combines **XGBoost**, **SMOTE**, **FastAPI**, **React**, **Vite**, **Axios**, and **SQLite** to create an end-to-end fraud detection platform with transaction analysis, risk scoring, prediction history, analytics, input validation, and cloud deployment.

> **Project type:** Machine Learning + Full-Stack Web Application  
> **Purpose:** Academic / educational / demonstration project

---

## 🌐 Live Application

| Service | Link |
|---|---|
| 🖥️ **Frontend** | https://fraud-transaction-detection-kj8o.onrender.com |
| ⚡ **Backend API** | https://fraudguard-api-wk9h.onrender.com |
| 📚 **Swagger API Docs** | https://fraudguard-api-wk9h.onrender.com/docs |
| 🐙 **GitHub Repository** | https://github.com/iamrudrapandey/Fraud-Transaction-Detection |

> **Note:** The backend is hosted on Render's free instance. After a period of inactivity, the first request may take some time because the service can spin down.

---

# ✨ Features

### 🤖 Machine Learning
- XGBoost-based fraud classification
- SMOTE for handling severe class imbalance
- RobustScaler preprocessing
- Optimized classification threshold
- Fraud probability calculation
- Risk-level classification

### 📊 Dashboard
- Total transactions analyzed
- Fraud transactions detected
- Legitimate transactions
- Fraud rate
- Recent prediction history
- Model performance information
- Interactive transaction scanner

### 🔍 Transaction Scanner
- Transaction input form
- `Time` and `V1–V28` feature support
- Transaction `Amount`
- Demo transaction loading
- Real-time prediction
- Fraud probability
- Risk level

### 🗄️ Database
- SQLite prediction history
- Transaction prediction records
- Fraud probability storage
- Risk-level storage
- Prediction timestamps
- Statistics API

### 🛡️ Validation & Error Handling
- Pydantic input validation
- Negative amount validation
- API error handling
- Database error handling
- Frontend API connection error handling
- CORS configuration

### 🚀 Deployment
- GitHub source control
- Render backend deployment
- Render frontend deployment
- HTTPS live API
- Swagger/OpenAPI documentation

---

# 🧠 Machine Learning

## Dataset

The project uses a credit-card transaction dataset containing:

- `Time`
- `V1` to `V28`
- `Amount`
- `Class`

The dataset is highly imbalanced, with legitimate transactions greatly outnumbering fraudulent transactions.

Large dataset files are intentionally **not stored in the GitHub repository** because GitHub has a 100 MB individual-file limit.

---

## 🔄 Machine Learning Pipeline

```text
Raw Transaction Dataset
          │
          ▼
     Data Cleaning
          │
          ▼
   Duplicate Handling
          │
          ▼
     Train / Test Split
          │
          ▼
   Feature Preprocessing
          │
          ▼
        SMOTE
          │
          ▼
     XGBoost Training
          │
          ▼
 Model Evaluation
          │
          ▼
 Threshold Optimization
          │
          ▼
 Saved Model Artifacts
          │
          ▼
 FastAPI Prediction API
```

---

# 📈 Model Performance

The final model achieved the following results on the project's evaluation setup:

| Metric | Score |
|---|---:|
| **Precision** | **92.50%** |
| **Recall** | **77.89%** |
| **F1 Score** | **84.57%** |
| Decision Threshold | **0.305818** |

### Why these metrics matter

**Precision**  
Measures how many transactions predicted as fraud were actually fraudulent.

**Recall**  
Measures how many actual fraudulent transactions were successfully detected.

**F1 Score**  
Provides a balance between Precision and Recall.

For fraud detection, both false positives and false negatives are important, so evaluating only accuracy would not be sufficient.

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │       USER          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   React Frontend    │
                    │     + Vite          │
                    └──────────┬──────────┘
                               │
                             Axios
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    └──────────┬──────────┘
                               │
                      Input Validation
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Prediction Module   │
                    │    predict.py       │
                    └──────────┬──────────┘
                               │
                    Preprocessing + Model
                               │
                               ▼
                    ┌─────────────────────┐
                    │   XGBoost Model     │
                    └──────────┬──────────┘
                               │
                    Fraud Probability
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Risk Classification │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │ SQLite Database │        │ React Dashboard │
        └─────────────────┘        └─────────────────┘
```

---

# 🔄 Application Workflow

```text
1. User enters transaction information
              ↓
2. React validates/submits the form
              ↓
3. Axios sends request to FastAPI
              ↓
4. FastAPI validates the request
              ↓
5. Prediction module preprocesses features
              ↓
6. XGBoost generates fraud probability
              ↓
7. Optimized threshold determines prediction
              ↓
8. Risk level is calculated
              ↓
9. Prediction is stored in SQLite
              ↓
10. Result is returned to React
              ↓
11. Dashboard displays the result
```

---

# 🧰 Technology Stack

## Frontend

| Technology | Purpose |
|---|---|
| **React** | User interface |
| **Vite** | Frontend build/development tool |
| **Axios** | API communication |
| **Recharts** | Charts and analytics |
| **CSS** | UI styling |

## Backend

| Technology | Purpose |
|---|---|
| **Python** | Backend and ML ecosystem |
| **FastAPI** | REST API |
| **Pydantic** | Request validation |
| **Uvicorn** | ASGI server |
| **SQLite** | Prediction storage |

## Machine Learning

| Technology | Purpose |
|---|---|
| **XGBoost** | Final classification model |
| **scikit-learn** | Preprocessing and evaluation |
| **imbalanced-learn** | SMOTE |
| **Pandas** | Data processing |
| **NumPy** | Numerical operations |
| **Joblib** | Model/scaler serialization |

## Deployment & Version Control

- Git
- GitHub
- Render

---

# 📂 Project Structure

```text
Fraud-Transaction-Detection/
│
├── backend/
│   └── main.py
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
├── src/
│   └── predict.py
│
├── models/
│   ├── optimized_xgboost.pkl
│   ├── robust_scaler.pkl
│   ├── final_threshold.pkl
│   └── other model artifacts
│
├── dataset/
│   └── creditcard.csv              # Not committed to GitHub
│
├── notebooks/
│   └── ML experiments / analysis
│
├── requirements.txt
├── .gitignore
└── README.md
```

> Large CSV files and unnecessary generated files are excluded through `.gitignore`.

---

# ⚙️ Local Installation

## 1. Clone the repository

```bash
git clone https://github.com/iamrudrapandey/Fraud-Transaction-Detection.git
```

```bash
cd Fraud-Transaction-Detection
```

---

## 2. Create a Python virtual environment

### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

If required, the main dependencies are:

```bash
pip install fastapi uvicorn pandas numpy scikit-learn xgboost imbalanced-learn pydantic joblib
```

---

# ⚡ Run the Backend

From the project root:

```bash
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

---

# 🌐 Run the Frontend

Open a second terminal.

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

Frontend:

```text
http://localhost:5173
```

---

# 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API information |
| `GET` | `/health` | API and database health |
| `POST` | `/predict` | Predict transaction fraud |
| `GET` | `/history` | Retrieve prediction history |
| `GET` | `/stats` | Retrieve transaction statistics |
| `DELETE` | `/history` | Clear prediction history |

---

# 📥 Prediction Input

The `/predict` endpoint accepts:

```text
Time
V1
V2
V3
...
V28
Amount
```

The model expects the same feature representation used during training.

---

# 📤 Example Prediction Response

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

# 🚦 Risk Classification

The application converts the model probability into an understandable risk level.

```text
Transaction
     │
     ▼
Fraud Probability
     │
     ▼
Risk Classification
     │
 ┌───┼───────────┐
 ▼   ▼           ▼
LOW MEDIUM      HIGH
```

The exact classification logic is implemented in the backend prediction pipeline.

---

# 🛡️ Input Validation

The backend uses Pydantic validation to ensure that incoming transaction data follows the expected format.

Examples of validation include:

- Required transaction fields
- Numeric feature validation
- Transaction amount validation
- Prevention of negative transaction amounts
- Invalid request handling

This helps prevent malformed data from being passed to the ML model.

---

# 🗄️ Database

FraudGuard AI uses **SQLite** for storing prediction history.

Stored information includes:

```text
Transaction Features
        +
Prediction
        +
Fraud Probability
        +
Risk Level
        +
Decision Threshold
        +
Timestamp
```

This allows the dashboard to display previous predictions and calculate transaction statistics.

---

# 🧪 Testing

The application was tested for:

### Backend

- API availability
- Health endpoint
- Valid prediction requests
- Invalid transaction inputs
- Database operations
- Prediction history
- Statistics
- CORS configuration

### Frontend

- Dashboard loading
- Transaction form
- API communication
- Prediction display
- Risk-level display
- History display
- Error messages
- Responsive UI

### Deployment

- Backend deployed successfully
- Frontend deployed successfully
- Frontend-to-backend communication verified
- Live health endpoint verified
- Production API tested

---

# 🚀 Deployment

## Backend

The FastAPI backend is deployed on **Render**.

Production API:

```text
https://fraudguard-api-wk9h.onrender.com
```

Swagger:

```text
https://fraudguard-api-wk9h.onrender.com/docs
```

## Frontend

The React/Vite frontend is deployed on **Render Static Site**.

Production frontend:

```text
https://fraud-transaction-detection-kj8o.onrender.com
```

## CORS

The backend allows the deployed frontend origin:

```text
https://fraud-transaction-detection-kj8o.onrender.com
```

along with local development origins.

---

# 📦 Model Artifacts

The prediction system uses serialized model artifacts such as:

```text
models/
├── optimized_xgboost.pkl
├── robust_scaler.pkl
├── final_threshold.pkl
└── other model files
```

The model, preprocessing pipeline, and threshold must remain compatible with the prediction code.

Large datasets such as:

```text
dataset/creditcard.csv
models/X_train.csv
models/X_test.csv
```

are excluded from the GitHub repository.

---

# 🔐 Security & Privacy

This project is intended for educational and demonstration purposes.

It should **not** be used as the sole decision-maker for real financial transactions.

A production fraud detection platform would require additional:

- Authentication
- Authorization
- Encryption
- Secure secret management
- Audit logging
- Rate limiting
- Monitoring
- Data privacy controls
- Regulatory compliance
- Model monitoring
- Fraud investigation workflows

---

# ⚠️ Limitations

- The model is trained on a fixed historical dataset.
- New fraud patterns may not be detected reliably without retraining.
- SQLite is suitable for this project but is not ideal for large-scale concurrent production workloads.
- The application is a demonstration system, not a production banking security platform.
- Render's free hosting can introduce cold-start delays after inactivity.
- Model performance can change when applied to a different transaction population.

---

# 🔮 Future Improvements

### Machine Learning

- Automated model retraining
- Hyperparameter optimization
- Model drift detection
- ROC-AUC visualization
- Confusion matrix
- Precision-Recall curve
- SHAP explainability
- Ensemble models

### Backend

- JWT authentication
- Role-based authorization
- PostgreSQL / cloud database
- API rate limiting
- Structured logging
- Background processing
- Docker deployment

### Frontend

- Advanced analytics
- Transaction filtering
- Export reports
- Better data visualization
- Admin dashboard
- User authentication

### Production

- CI/CD pipeline
- Automated testing
- Monitoring and alerting
- Secure secret management
- Cloud object storage for model artifacts
- Scalable infrastructure

---

# 💡 Key Learning Outcomes

Through this project, the following concepts were implemented:

- Machine learning classification
- Imbalanced dataset handling
- SMOTE
- XGBoost
- Feature preprocessing
- Model evaluation
- Threshold optimization
- REST API development
- Pydantic validation
- React frontend development
- Axios API integration
- SQLite database integration
- CORS configuration
- Git and GitHub
- Cloud deployment
- Full-stack ML application development

---

# 📌 Project Highlights

> **XGBoost + SMOTE + FastAPI + React + SQLite**

**Model F1 Score:** `84.57%`

**Precision:** `92.50%`

**Recall:** `77.89%`

**Decision Threshold:** `0.305818`

**Deployment:** GitHub + Render

---

# 👨‍💻 Author

### Rudra

**AI / ML & Full-Stack Project**

GitHub:

https://github.com/iamrudrapandey

---

# ⭐ Project Summary

**FraudGuard AI** demonstrates how a machine-learning model can be transformed into a complete web application.

The project covers the complete pipeline:

```text
Data
 ↓
Preprocessing
 ↓
SMOTE
 ↓
XGBoost
 ↓
Evaluation
 ↓
FastAPI
 ↓
React
 ↓
SQLite
 ↓
GitHub
 ↓
Render
 ↓
Live Application
```

The project provides a practical demonstration of integrating **machine learning, backend APIs, frontend development, database management, validation, version control, and cloud deployment** into a single application.

---

## 📜 Disclaimer

FraudGuard AI is an academic/educational project. Its predictions should not be treated as guaranteed fraud determinations or used as the sole basis for real financial decisions.
