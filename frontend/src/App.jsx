import { useEffect, useState } from "react";
import axios from "axios";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import "./App.css";

const API_URL = "http://127.0.0.1:8000";

/* ============================================================
   DEFAULT / DEMO TRANSACTION
   ============================================================ */

const initialTransaction = {
  Time: 406,
  V1: -1.359807,
  V2: -0.072781,
  V3: 2.536347,
  V4: 1.378155,
  V5: -0.338321,
  V6: 0.462388,
  V7: 0.239599,
  V8: 0.098698,
  V9: 0.363787,
  V10: 0.090794,
  V11: -0.5516,
  V12: -0.617801,
  V13: -0.99139,
  V14: -0.311169,
  V15: 1.468177,
  V16: -0.4704,
  V17: 0.207971,
  V18: 0.025791,
  V19: 0.403993,
  V20: 0.251412,
  V21: -0.018307,
  V22: 0.277838,
  V23: 0.066928,
  V24: 0.066928,
  V25: 0.128539,
  V26: -0.189115,
  V27: 0.133558,
  V28: -0.021053,
  Amount: 149.62,
};

/* ============================================================
   APP
   ============================================================ */

function App() {
  const [activePage, setActivePage] = useState("overview");

  const [transaction, setTransaction] =
    useState({ ...initialTransaction });

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const [history, setHistory] = useState([]);

  const [stats, setStats] = useState({
    total: 0,
    fraud: 0,
    legitimate: 0,
    fraud_rate: 0,
  });

  const [apiOnline, setApiOnline] = useState(false);

  const [databaseOnline, setDatabaseOnline] =
    useState(false);

  /* ============================================================
     INPUT VALIDATION STATE
     ============================================================ */

  const [errors, setErrors] = useState({});

  const [apiError, setApiError] = useState("");

  /* ============================================================
     VALIDATE SINGLE FIELD
     ============================================================ */

  const validateField = (name, value) => {
    if (value === "" || value === null || value === undefined) {
      return "This field is required.";
    }

    const numberValue = Number(value);

    if (!Number.isFinite(numberValue)) {
      return "Please enter a valid number.";
    }

    if (name === "Amount" && numberValue < 0) {
      return "Amount cannot be negative.";
    }

    return "";
  };

  /* ============================================================
     VALIDATE COMPLETE TRANSACTION
     ============================================================ */

  const validateTransaction = () => {
    const newErrors = {};

    Object.entries(transaction).forEach(
      ([name, value]) => {
        const error = validateField(
          name,
          value
        );

        if (error) {
          newErrors[name] = error;
        }
      }
    );

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  /* ============================================================
     CHECK API
     ============================================================ */

  const checkApiStatus = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/health`,
        {
          timeout: 5000,
        }
      );

      setApiOnline(true);

      setDatabaseOnline(
        response.data?.database === "connected"
      );

      setApiError("");

      return true;
    } catch (error) {
      console.error(
        "API connection error:",
        error
      );

      setApiOnline(false);
      setDatabaseOnline(false);

      setApiError(
        "Unable to connect to the Fraud Detection API."
      );

      return false;
    }
  };

  /* ============================================================
     LOAD HISTORY + STATS
     ============================================================ */

  const loadDatabaseData = async () => {
    try {
      const [
        historyResponse,
        statsResponse,
      ] = await Promise.all([
        axios.get(`${API_URL}/history`, {
          timeout: 5000,
        }),

        axios.get(`${API_URL}/stats`, {
          timeout: 5000,
        }),
      ]);

      const databaseHistory =
        historyResponse.data?.history || [];

      const formattedHistory =
        databaseHistory.map((item) => ({
          id: item.id,

          prediction: item.prediction,

          probability:
            Number(
              item.fraud_probability
            ) || 0,

          risk:
            item.risk_level || "UNKNOWN",

          amount:
            Number(item.Amount) || 0,

          time:
            item.created_at
              ? new Date(
                  item.created_at
                ).toLocaleTimeString()
              : "--",
        }));

      setHistory(formattedHistory);

      const databaseStats =
        statsResponse.data || {};

      setStats({
        total:
          Number(databaseStats.total) || 0,

        fraud:
          Number(databaseStats.fraud) || 0,

        legitimate:
          Number(
            databaseStats.legitimate
          ) || 0,

        fraud_rate:
          Number(
            databaseStats.fraud_rate
          ) || 0,
      });

      setDatabaseOnline(true);

    } catch (error) {
      console.error(
        "Unable to load database data:",
        error
      );

      setDatabaseOnline(false);

      if (
        error.code === "ECONNABORTED"
      ) {
        setApiError(
          "Database request timed out."
        );
      }
    }
  };

  /* ============================================================
     INITIAL LOAD
     ============================================================ */

  useEffect(() => {
    const initializeApp = async () => {
      const online =
        await checkApiStatus();

      if (online) {
        await loadDatabaseData();
      }
    };

    initializeApp();
  }, []);

  /* ============================================================
     INPUT CHANGE
     ============================================================ */

  const handleChange = (e) => {
    const {
      name,
      value,
    } = e.target;

    const convertedValue =
      value === ""
        ? ""
        : Number(value);

    setTransaction(
      (previous) => ({
        ...previous,
        [name]: convertedValue,
      })
    );

    /*
      Clear the error for this field
      as soon as the user starts correcting it.
    */

    setErrors(
      (previous) => ({
        ...previous,
        [name]: "",
      })
    );

    setApiError("");
  };

  /* ============================================================
     INPUT BLUR VALIDATION
     ============================================================ */

  const handleBlur = (e) => {
    const {
      name,
      value,
    } = e.target;

    const error =
      validateField(
        name,
        value
      );

    setErrors(
      (previous) => ({
        ...previous,
        [name]: error,
      })
    );
  };

  /* ============================================================
     RESET
     ============================================================ */

  const resetTransaction = () => {
    setTransaction({
      ...initialTransaction,
    });

    setResult(null);

    setErrors({});

    setApiError("");
  };

  /* ============================================================
     LOAD DEMO
     ============================================================ */

  const loadDemo = () => {
    setTransaction({
      ...initialTransaction,
    });

    setResult(null);

    setErrors({});

    setApiError("");
  };

  /* ============================================================
     ANALYZE TRANSACTION
     ============================================================ */

  const analyzeTransaction = async () => {

    /*
      Validate everything before
      sending request to backend.
    */

    const isValid =
      validateTransaction();

    if (!isValid) {
      setApiError(
        "Please correct the highlighted fields before analyzing."
      );

      return;
    }

    setLoading(true);

    setResult(null);

    setApiError("");

    try {
      const response =
        await axios.post(
          `${API_URL}/predict`,
          transaction,
          {
            timeout: 15000,
          }
        );

      const data =
        response.data;

      console.log(
        "Prediction result:",
        data
      );

      setResult(data);

      setApiOnline(true);

      if (
        data.saved_to_database
      ) {
        setDatabaseOnline(true);
      }

      await loadDatabaseData();

    } catch (error) {

      console.error(
        "Prediction error:",
        error
      );

      /*
        Backend returned an HTTP response.
      */

      if (error.response) {

        const status =
          error.response.status;

        const backendData =
          error.response.data;

        if (status === 422) {

          setApiError(
            backendData?.message ||
              "Please check the transaction data."
          );

        } else if (
          status === 500
        ) {

          const detail =
            backendData?.detail;

          if (
            typeof detail ===
            "object"
          ) {
            setApiError(
              detail.message ||
                "Server error while processing the transaction."
            );
          } else {
            setApiError(
              "Server error while processing the transaction."
            );
          }

        } else {

          setApiError(
            backendData?.message ||
              backendData?.detail ||
              "An unexpected API error occurred."
          );
        }

        setApiOnline(true);

      } else if (
        error.code ===
        "ECONNABORTED"
      ) {

        setApiError(
          "The request timed out. Please try again."
        );

        setApiOnline(false);

      } else if (
        error.request
      ) {

        setApiError(
          "Cannot connect to the Fraud Detection API. Make sure FastAPI is running."
        );

        setApiOnline(false);

      } else {

        setApiError(
          "Something went wrong. Please try again."
        );
      }

    } finally {
      setLoading(false);
    }
  };

  /* ============================================================
     CLEAR HISTORY
     ============================================================ */

  const clearHistory = async () => {

    const confirmed =
      window.confirm(
        "Are you sure you want to delete all prediction history?"
      );

    if (!confirmed) {
      return;
    }

    try {

      await axios.delete(
        `${API_URL}/history`,
        {
          timeout: 10000,
        }
      );

      setHistory([]);

      setStats({
        total: 0,
        fraud: 0,
        legitimate: 0,
        fraud_rate: 0,
      });

      setResult(null);

      setDatabaseOnline(true);

      setApiError("");

    } catch (error) {

      console.error(
        "Clear history error:",
        error
      );

      setDatabaseOnline(false);

      if (error.response) {

        setApiError(
          error.response.data?.message ||
            "Unable to clear database history."
        );

      } else {

        setApiError(
          "Unable to connect to the database."
        );
      }
    }
  };

  /* ============================================================
     CALCULATIONS
     ============================================================ */

  const probability = result
    ? Number(
        result.fraud_probability_percent
      ) || 0
    : 0;

  const safeProbability =
    Math.min(
      Math.max(
        probability,
        0
      ),
      100
    );

  const gaugeDegree =
    safeProbability * 3.6;

  const fraudRate =
    stats.total > 0
      ? (
          (stats.fraud /
            stats.total) *
          100
        ).toFixed(1)
      : "0.0";

  const chartData = [
    {
      name: "Legitimate",
      value: stats.legitimate,
    },
    {
      name: "Fraud",
      value: stats.fraud,
    },
  ];

  /* ============================================================
     RENDER
     ============================================================ */

  return (
    <div className="app">

      {/* ======================================================
          SIDEBAR
      ====================================================== */}

      <aside className="sidebar">

        <div className="sidebar-logo">

          <div className="logo-icon">
            🛡️
          </div>

          <div>
            <strong>
              FraudGuard
            </strong>

            <span>
              AI Security
            </span>
          </div>

        </div>

        <div className="sidebar-section">

          <span className="sidebar-title">
            MAIN MENU
          </span>

          <button
            className={
              activePage === "overview"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              setActivePage(
                "overview"
              )
            }
          >
            <span>⌂</span>
            Overview
          </button>

          <button
            className={
              activePage === "scanner"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              setActivePage(
                "scanner"
              )
            }
          >
            <span>⌕</span>
            Transaction Scanner
          </button>

          <button
            className={
              activePage === "history"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              setActivePage(
                "history"
              )
            }
          >
            <span>◷</span>
            Prediction History
          </button>

          <button
            className={
              activePage === "model"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              setActivePage(
                "model"
              )
            }
          >
            <span>◈</span>
            Model Performance
          </button>

        </div>

        <div className="sidebar-bottom">

          <div className="system-status">

            <span
              className={
                apiOnline
                  ? "status-dot online"
                  : "status-dot offline"
              }
            />

            <div>

              <strong>
                {apiOnline
                  ? "System Online"
                  : "System Offline"}
              </strong>

              <small>
                {databaseOnline
                  ? "API + SQLite Connected"
                  : apiOnline
                  ? "API Connected"
                  : "API Disconnected"}
              </small>

            </div>

          </div>

          <div className="sidebar-version">
            FraudGuard AI
            <span>
              v1.0.0
            </span>
          </div>

        </div>

      </aside>

      {/* ======================================================
          MAIN CONTENT
      ====================================================== */}

      <div className="main-content">

        {/* ====================================================
            TOP BAR
        ==================================================== */}

        <header className="topbar">

          <div>

            <span className="breadcrumb">
              AI FRAUD DETECTION
            </span>

            <h1>
              {activePage ===
                "overview" &&
                "Dashboard Overview"}

              {activePage ===
                "scanner" &&
                "Transaction Scanner"}

              {activePage ===
                "history" &&
                "Prediction History"}

              {activePage ===
                "model" &&
                "Model Performance"}
            </h1>

          </div>

          <div className="topbar-right">

            <div className="api-status">

              <span
                className={
                  apiOnline
                    ? "status-dot online"
                    : "status-dot offline"
                }
              />

              <div>

                <strong>
                  {apiOnline
                    ? "API Online"
                    : "API Offline"}
                </strong>

                <small>
                  {databaseOnline
                    ? "SQLite Connected"
                    : "SQLite Disconnected"}
                </small>

              </div>

            </div>

            <div className="model-version">

              <span>
                MODEL
              </span>

              <strong>
                XGBoost
              </strong>

            </div>

          </div>

        </header>

        {/* ====================================================
            GLOBAL ERROR MESSAGE
        ==================================================== */}

        {apiError && (

          <div
            className="api-error-box"
            role="alert"
          >

            <span>
              ⚠️
            </span>

            <div>
              <strong>
                Error
              </strong>

              <p>
                {apiError}
              </p>
            </div>

            <button
              onClick={() =>
                setApiError("")
              }
            >
              ×
            </button>

          </div>

        )}

        {/* ====================================================
            OVERVIEW
        ==================================================== */}

        {activePage ===
          "overview" && (

          <div className="page">

            <section className="hero-card">

              <div className="hero-content">

                <span className="hero-label">
                  ✦ MACHINE LEARNING SECURITY
                </span>

                <h2>
                  Intelligent fraud detection
                  <br />
                  <span>
                    powered by AI.
                  </span>
                </h2>

                <p>
                  Analyze credit card
                  transactions using
                  XGBoost machine learning
                  with SMOTE class balancing.
                </p>

                <button
                  className="hero-button"
                  onClick={() =>
                    setActivePage(
                      "scanner"
                    )
                  }
                >
                  Start Transaction Scan →
                </button>

              </div>

              <div className="hero-visual">

                <div className="hero-shield">
                  🛡️
                </div>

                <div className="orbit orbit-one"></div>
                <div className="orbit orbit-two"></div>

              </div>

            </section>

            <section className="stats-grid">

              <div className="dashboard-stat">

                <div className="stat-top">
                  <span>
                    TOTAL ANALYZED
                  </span>

                  <div className="stat-icon blue">
                    ◉
                  </div>
                </div>

                <strong>
                  {stats.total}
                </strong>

                <small>
                  Transactions scanned
                </small>

              </div>

              <div className="dashboard-stat">

                <div className="stat-top">
                  <span>
                    FRAUD DETECTED
                  </span>

                  <div className="stat-icon red">
                    ⚠
                  </div>
                </div>

                <strong>
                  {stats.fraud}
                </strong>

                <small>
                  Suspicious transactions
                </small>

              </div>

              <div className="dashboard-stat">

                <div className="stat-top">
                  <span>
                    LEGITIMATE
                  </span>

                  <div className="stat-icon green">
                    ✓
                  </div>
                </div>

                <strong>
                  {stats.legitimate}
                </strong>

                <small>
                  Safe transactions
                </small>

              </div>

              <div className="dashboard-stat">

                <div className="stat-top">
                  <span>
                    FRAUD RATE
                  </span>

                  <div className="stat-icon purple">
                    %
                  </div>
                </div>

                <strong>
                  {fraudRate}%
                </strong>

                <small>
                  Current database
                </small>

              </div>

            </section>

            <section className="overview-grid">

              <div className="panel quick-panel">

                <div className="panel-heading">

                  <div>

                    <span className="section-label">
                      QUICK ACTION
                    </span>

                    <h2>
                      Scan a Transaction
                    </h2>

                  </div>

                  <span className="panel-icon">
                    🔍
                  </span>

                </div>

                <p>
                  Enter transaction features
                  and let the AI model determine
                  whether the transaction is
                  legitimate or potentially
                  fraudulent.
                </p>

                <button
                  className="primary-button"
                  onClick={() =>
                    setActivePage(
                      "scanner"
                    )
                  }
                >
                  Open Scanner
                </button>

              </div>

              <div className="panel model-summary">

                <div className="panel-heading">

                  <div>

                    <span className="section-label">
                      MODEL
                    </span>

                    <h2>
                      XGBoost Classifier
                    </h2>

                  </div>

                  <span className="model-badge">
                    ACTIVE
                  </span>

                </div>

                <div className="mini-metrics">

                  <div>
                    <span>
                      Precision
                    </span>

                    <strong>
                      92.50%
                    </strong>
                  </div>

                  <div>
                    <span>
                      Recall
                    </span>

                    <strong>
                      77.89%
                    </strong>
                  </div>

                  <div>
                    <span>
                      F1 Score
                    </span>

                    <strong>
                      84.57%
                    </strong>
                  </div>

                </div>

              </div>

            </section>

            <section className="panel">

              <div className="panel-heading">

                <div>

                  <span className="section-label">
                    RECENT ACTIVITY
                  </span>

                  <h2>
                    Latest Predictions
                  </h2>

                </div>

                <button
                  className="text-button"
                  onClick={() =>
                    setActivePage(
                      "history"
                    )
                  }
                >
                  View All →
                </button>

              </div>

              {history.length === 0 ? (

                <div className="empty-history">

                  <div>
                    📋
                  </div>

                  <strong>
                    No predictions yet
                  </strong>

                  <span>
                    Run your first transaction
                    analysis.
                  </span>

                </div>

              ) : (

                <div className="activity-list">

                  {history
                    .slice(0, 5)
                    .map((item) => (

                      <div
                        className="activity-item"
                        key={item.id}
                      >

                        <div
                          className={
                            item.prediction ===
                            "FRAUD"
                              ? "activity-icon fraud"
                              : "activity-icon safe"
                          }
                        >
                          {item.prediction ===
                          "FRAUD"
                            ? "!"
                            : "✓"}
                        </div>

                        <div className="activity-main">

                          <strong>
                            {item.prediction}
                          </strong>

                          <span>
                            Amount: $
                            {Number(
                              item.amount
                            ).toFixed(2)}
                          </span>

                        </div>

                        <div className="activity-probability">

                          <strong>
                            {item.probability}%
                          </strong>

                          <span>
                            {item.risk} risk
                          </span>

                        </div>

                        <span className="activity-time">
                          {item.time}
                        </span>

                      </div>

                    ))}

                </div>

              )}

            </section>

          </div>
        )}

        {/* ====================================================
            SCANNER
        ==================================================== */}

        {activePage ===
          "scanner" && (

          <div className="page">

            <div className="scanner-layout">

              {/* INPUT */}

              <section className="panel scanner-panel">

                <div className="panel-heading">

                  <div>

                    <span className="section-label">
                      TRANSACTION INPUT
                    </span>

                    <h2>
                      Transaction Features
                    </h2>

                    <p>
                      Enter the transaction values
                      for analysis.
                    </p>

                  </div>

                  <button
                    className="secondary-button"
                    onClick={loadDemo}
                  >
                    ↻ Demo
                  </button>

                </div>

                {/* AMOUNT */}

                <div className="amount-card">

                  <div className="amount-input-wrapper">

                    <span>
                      TRANSACTION AMOUNT
                    </span>

                    <div
                      className={
                        errors.Amount
                          ? "amount-input-box input-error"
                          : "amount-input-box"
                      }
                    >

                      <span className="currency-symbol">
                        $
                      </span>

                      <input
                        type="number"
                        name="Amount"
                        min="0"
                        step="0.01"
                        value={
                          transaction.Amount
                        }
                        onChange={
                          handleChange
                        }
                        onBlur={
                          handleBlur
                        }
                        placeholder="Enter amount"
                        aria-invalid={
                          Boolean(
                            errors.Amount
                          )
                        }
                      />

                    </div>

                    <small>
                      Enter any transaction amount
                    </small>

                    {errors.Amount && (

                      <div className="field-error">
                        ⚠ {errors.Amount}
                      </div>

                    )}

                  </div>

                  <div className="amount-card-icon">
                    💳
                  </div>

                </div>

                {/* FEATURES */}

                <div className="features-title">
                  PCA Features & Transaction Data
                </div>

                <div className="form-grid">

                  {Object.keys(transaction)
                    .filter(
                      (feature) =>
                        feature !== "Amount"
                    )
                    .map(
                      (feature) => (

                        <div
                          className="input-group"
                          key={feature}
                        >

                          <label>
                            {feature}
                          </label>

                          <input
                            className={
                              errors[feature]
                                ? "field-invalid"
                                : ""
                            }
                            type="number"
                            step="any"
                            name={feature}
                            value={
                              transaction[
                                feature
                              ]
                            }
                            onChange={
                              handleChange
                            }
                            onBlur={
                              handleBlur
                            }
                            aria-invalid={
                              Boolean(
                                errors[
                                  feature
                                ]
                              )
                            }
                          />

                          {errors[
                            feature
                          ] && (

                            <small className="field-error">
                              ⚠{" "}
                              {
                                errors[
                                  feature
                                ]
                              }
                            </small>

                          )}

                        </div>

                      )
                    )}

                </div>

                <div className="scanner-actions">

                  <button
                    className="secondary-button"
                    onClick={
                      resetTransaction
                    }
                  >
                    Reset
                  </button>

                  <button
                    className="primary-button analyze"
                    onClick={
                      analyzeTransaction
                    }
                    disabled={
                      loading
                    }
                  >

                    {loading ? (

                      <>
                        <span className="spinner"></span>
                        Analyzing...
                      </>

                    ) : (

                      <>
                        🔍 Analyze Transaction
                      </>

                    )}

                  </button>

                </div>

              </section>

              {/* RESULT */}

              <section className="panel scanner-result">

                <div className="panel-heading">

                  <div>

                    <span className="section-label">
                      AI DECISION
                    </span>

                    <h2>
                      Analysis Result
                    </h2>

                  </div>

                  {result && (

                    <span className="live-badge">
                      ● LIVE
                    </span>

                  )}

                </div>

                {!result ? (

                  <div className="scanner-empty">

                    <div className="large-shield">
                      🛡️
                    </div>

                    <h3>
                      Ready to Scan
                    </h3>

                    <p>
                      Submit a transaction
                      to receive an instant
                      AI-powered risk assessment.
                    </p>

                  </div>

                ) : (

                  <div className="result-content">

                    <div
                      className={
                        result.prediction ===
                        "FRAUD"
                          ? "result-banner fraud"
                          : "result-banner safe"
                      }
                    >

                      <div className="result-status-icon">

                        {result.prediction ===
                        "FRAUD"
                          ? "⚠"
                          : "✓"}

                      </div>

                      <div>

                        <span>
                          AI PREDICTION
                        </span>

                        <strong>
                          {result.prediction}
                        </strong>

                      </div>

                    </div>

                    <div className="gauge-section">

                      <span>
                        FRAUD PROBABILITY
                      </span>

                      <div className="gauge-container">

                        <div
                          className="gauge-circle"
                          style={{
                            background:
                              `conic-gradient(${
                                result.prediction ===
                                "FRAUD"
                                  ? "#ef4444"
                                  : "#22c55e"
                              } 0deg ${gaugeDegree}deg, #263449 ${gaugeDegree}deg 360deg)`,
                          }}
                        >

                          <div className="gauge-inner">

                            <strong>
                              {safeProbability}%
                            </strong>

                            <small>
                              FRAUD RISK
                            </small>

                          </div>

                        </div>

                      </div>

                    </div>

                    <div className="result-info">

                      <div>

                        <span>
                          Risk Level
                        </span>

                        <strong
                          className={`risk-badge ${
                            String(
                              result.risk_level ||
                                ""
                            ).toLowerCase()
                          }`}
                        >
                          {result.risk_level}
                        </strong>

                      </div>

                      <div>

                        <span>
                          Threshold
                        </span>

                        <strong>
                          {result.threshold}
                        </strong>

                      </div>

                    </div>

                    <div className="database-result-status">

                      {result.saved_to_database ? (

                        <>
                          ✓ Saved to SQLite Database
                          {result.database_id
                            ? ` • ID: ${result.database_id}`
                            : ""}
                        </>

                      ) : (

                        <>
                          ⚠ Prediction completed,
                          but database save was not confirmed.
                        </>

                      )}

                    </div>

                    <div
                      className={
                        result.prediction ===
                        "FRAUD"
                          ? "alert-box fraud-alert"
                          : "alert-box safe-alert"
                      }
                    >

                      <strong>

                        {result.prediction ===
                        "FRAUD"
                          ? "⚠ Suspicious Transaction Detected"
                          : "✓ Transaction Appears Legitimate"}

                      </strong>

                      <small>

                        {result.prediction ===
                        "FRAUD"
                          ? "Further verification is recommended before approving this transaction."
                          : "The model found no significant fraud indicators in this transaction."}

                      </small>

                    </div>

                    <div className="risk-explanation">

                      <h3>
                        Risk Assessment
                      </h3>

                      <p>

                        {result.prediction ===
                        "FRAUD"
                          ? "The model identified patterns that are associated with fraudulent transactions."
                          : "The model identified patterns that are consistent with legitimate transactions."}

                      </p>

                    </div>

                  </div>

                )}

              </section>

            </div>

          </div>
        )}

        {/* ====================================================
            HISTORY
        ==================================================== */}

        {activePage ===
          "history" && (

          <div className="page">

            <section className="panel">

              <div className="panel-heading">

                <div>

                  <span className="section-label">
                    TRANSACTION LOG
                  </span>

                  <h2>
                    Prediction History
                  </h2>

                  <p>
                    All transactions stored
                    in the SQLite database.
                  </p>

                </div>

                {history.length > 0 && (

                  <button
                    className="danger-button"
                    onClick={
                      clearHistory
                    }
                  >
                    Clear History
                  </button>

                )}

              </div>

              {history.length ===
              0 ? (

                <div className="empty-history large">

                  <div>
                    📋
                  </div>

                  <strong>
                    No transaction history
                  </strong>

                  <span>
                    Analyze a transaction to
                    create your first record.
                  </span>

                </div>

              ) : (

                <div className="history-table">

                  <div className="history-row history-title">

                    <span>#</span>
                    <span>Prediction</span>
                    <span>Amount</span>
                    <span>Probability</span>
                    <span>Risk</span>
                    <span>Time</span>

                  </div>

                  {history.map(
                    (
                      item,
                      index
                    ) => (

                      <div
                        className="history-row"
                        key={item.id}
                      >

                        <span>
                          {index + 1}
                        </span>

                        <span
                          className={
                            item.prediction ===
                            "FRAUD"
                              ? "fraud-text"
                              : "legitimate-text"
                          }
                        >

                          {item.prediction ===
                          "FRAUD"
                            ? "⚠ FRAUD"
                            : "✓ LEGITIMATE"}

                        </span>

                        <span>
                          $
                          {Number(
                            item.amount
                          ).toFixed(2)}
                        </span>

                        <span>
                          {item.probability}%
                        </span>

                        <span>
                          {item.risk}
                        </span>

                        <span>
                          {item.time}
                        </span>

                      </div>

                    )
                  )}

                </div>

              )}

            </section>

            <section className="panel analytics-panel">

              <h2>
                📊 Transaction Analytics
              </h2>

              <div className="analytics-grid">

                <div className="chart-card">

                  <h3>
                    Fraud vs Legitimate
                  </h3>

                  {stats.total ===
                  0 ? (

                    <p>
                      Analyze a transaction
                      to see analytics.
                    </p>

                  ) : (

                    <ResponsiveContainer
                      width="100%"
                      height={280}
                    >

                      <PieChart>

                        <Pie
                          data={
                            chartData
                          }
                          dataKey="value"
                          nameKey="name"
                          cx="50%"
                          cy="50%"
                          innerRadius={55}
                          outerRadius={90}
                        >

                          <Cell fill="#22c55e" />
                          <Cell fill="#ef4444" />

                        </Pie>

                        <Tooltip />

                      </PieChart>

                    </ResponsiveContainer>

                  )}

                </div>

                <div className="analytics-summary">

                  <div className="analytics-number">

                    <span>
                      Total Transactions
                    </span>

                    <strong>
                      {stats.total}
                    </strong>

                  </div>

                  <div className="analytics-number">

                    <span>
                      Fraud Detected
                    </span>

                    <strong>
                      {stats.fraud}
                    </strong>

                  </div>

                  <div className="analytics-number">

                    <span>
                      Legitimate
                    </span>

                    <strong>
                      {stats.legitimate}
                    </strong>

                  </div>

                </div>

              </div>

            </section>

          </div>

        )}

        {/* ====================================================
            MODEL PERFORMANCE
        ==================================================== */}

        {activePage ===
          "model" && (

          <div className="page">

            <section className="panel model-page">

              <div className="model-hero">

                <div>

                  <span className="section-label">
                    MACHINE LEARNING
                  </span>

                  <h2>
                    Model Performance
                  </h2>

                  <p>
                    Optimized XGBoost fraud
                    detection model trained
                    with SMOTE.
                  </p>

                </div>

                <div className="model-active">
                  ● MODEL ACTIVE
                </div>

              </div>

              <div className="performance-grid">

                <div className="performance-card">

                  <span>
                    PRECISION
                  </span>

                  <strong>
                    92.50%
                  </strong>

                  <div className="metric-bar">

                    <div
                      style={{
                        width:
                          "92.5%",
                      }}
                    />

                  </div>

                  <small>
                    Accurate fraud predictions
                  </small>

                </div>

                <div className="performance-card">

                  <span>
                    RECALL
                  </span>

                  <strong>
                    77.89%
                  </strong>

                  <div className="metric-bar">

                    <div
                      style={{
                        width:
                          "77.89%",
                      }}
                    />

                  </div>

                  <small>
                    Fraud detection capability
                  </small>

                </div>

                <div className="performance-card">

                  <span>
                    F1 SCORE
                  </span>

                  <strong>
                    84.57%
                  </strong>

                  <div className="metric-bar">

                    <div
                      style={{
                        width:
                          "84.57%",
                      }}
                    />

                  </div>

                  <small>
                    Balanced performance
                  </small>

                </div>

              </div>

              <div className="model-details">

                <div>
                  <span>
                    Algorithm
                  </span>

                  <strong>
                    XGBoost Classifier
                  </strong>
                </div>

                <div>
                  <span>
                    Imbalance Handling
                  </span>

                  <strong>
                    SMOTE
                  </strong>
                </div>

                <div>
                  <span>
                    Decision Threshold
                  </span>

                  <strong>
                    0.305818
                  </strong>
                </div>

                <div>
                  <span>
                    Training Strategy
                  </span>

                  <strong>
                    Balanced Classification
                  </strong>
                </div>

              </div>

              <div className="model-explanation">

                <h3>
                  About the Model
                </h3>

                <p>
                  The fraud detection system uses
                  XGBoost with SMOTE-based class
                  balancing to handle the highly
                  imbalanced transaction dataset.
                  The optimized decision threshold
                  is used to improve fraud
                  classification performance.
                </p>

              </div>

            </section>

          </div>

        )}

        {/* ====================================================
            FOOTER
        ==================================================== */}

        <footer>

          <div>
            🛡️ FraudGuard AI
          </div>

          <span>
            XGBoost + SMOTE • FastAPI • React • SQLite
          </span>

          <small>
            AI-powered credit card fraud detection
          </small>

        </footer>

      </div>

    </div>
  );
}

export default App;