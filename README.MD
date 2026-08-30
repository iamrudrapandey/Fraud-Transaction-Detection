# 🛡️ FraudGuard AI

## AI-Powered Credit Card Fraud Detection System

FraudGuard AI is a machine-learning-powered web application that analyzes credit card transactions and predicts whether a transaction is **LEGITIMATE** or **FRAUD**.

The project combines **XGBoost, SMOTE, FastAPI, React, SQLite, and Vite** to provide real-time fraud detection, risk assessment, prediction history, and transaction analytics.

---

## 🚀 Live Demo

### Frontend
https://fraud-transaction-detection-kj8o.onrender.com

### Backend API
https://fraudguard-api-wk9h.onrender.com

### API Health Check
https://fraudguard-api-wk9h.onrender.com/health

### API Documentation
https://fraudguard-api-wk9h.onrender.com/docs

---

# ✨ Features

- 🤖 AI-powered credit card fraud detection
- 📊 XGBoost classification model
- ⚖️ SMOTE for handling class imbalance
- 🔍 Real-time transaction analysis
- 📈 Fraud probability calculation
- 🚦 Risk-level classification
- 💾 SQLite prediction history
- 📊 Fraud and legitimate transaction statistics
- 🩺 API health monitoring
- ⚡ React + Vite frontend
- 🚀 FastAPI backend
- ✅ Input validation
- 🛡️ Backend error handling
- 📱 Responsive dashboard

---

# 🧠 Machine Learning

FraudGuard AI uses an **XGBoost Classifier** for fraud detection.

The dataset contains highly imbalanced transaction classes, where legitimate transactions are much more common than fraudulent transactions.

To address this problem, **SMOTE (Synthetic Minority Over-sampling Technique)** is used during model training.

## Model Performance

| Metric | Score |
|---|---:|
| Precision | 92.50% |
| Recall | 77.89% |
| F1 Score | 84.57% |

### Decision Threshold

```text
0.305818