from pathlib import Path
import joblib
import numpy as np
import pandas as pd


# ============================================================
# PATHS
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = ROOT_DIR / "models"


# ============================================================
# LOAD MODEL
# ============================================================

MODEL_PATH = MODEL_DIR / "optimized_xgboost.pkl"
SCALER_PATH = MODEL_DIR / "robust_scaler.pkl"
THRESHOLD_PATH = MODEL_DIR / "final_threshold.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
threshold_data = joblib.load(THRESHOLD_PATH)

THRESHOLD = float(threshold_data["threshold"])


# ============================================================
# EXACT FEATURES USED BY XGBOOST
# ============================================================

FEATURES = [
    "V1", "V2", "V3", "V4", "V5", "V6",
    "V7", "V8", "V9", "V10", "V11", "V12",
    "V13", "V14", "V15", "V16", "V17", "V18",
    "V19", "V20", "V21", "V22", "V23", "V24",
    "V25", "V26", "V27", "V28",
    "Amount",
    "Time_sin",
    "Time_cos"
]


# ============================================================
# PREPROCESS TRANSACTION
# ============================================================

def preprocess_transaction(transaction):

    data = pd.DataFrame([transaction])

    # --------------------------------------------------------
    # Create cyclical Time features
    # --------------------------------------------------------

    seconds_per_day = 24 * 60 * 60

    time_seconds = (
        data["Time"] % seconds_per_day
    )

    data["Time_sin"] = np.sin(
        2 * np.pi *
        time_seconds /
        seconds_per_day
    )

    data["Time_cos"] = np.cos(
        2 * np.pi *
        time_seconds /
        seconds_per_day
    )

    # --------------------------------------------------------
    # Scale Amount
    # --------------------------------------------------------

    data[["Amount"]] = scaler.transform(
        data[["Amount"]]
    )

    # --------------------------------------------------------
    # Select EXACT model features
    # --------------------------------------------------------

    data = data[FEATURES]

    return data


# ============================================================
# PREDICT
# ============================================================

def predict_transaction(transaction):

    X = preprocess_transaction(
        transaction
    )

    probability = float(
        model.predict_proba(X)[0][1]
    )

    prediction = int(
        probability >= THRESHOLD
    )

    # --------------------------------------------------------
    # Risk level
    # --------------------------------------------------------

    if probability >= 0.80:

        risk_level = "HIGH"

    elif probability >= THRESHOLD:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    return {
        "prediction": (
            "FRAUD"
            if prediction == 1
            else "LEGITIMATE"
        ),
        "fraud_probability": round(
            probability,
            6
        ),
        "fraud_probability_percent": round(
            probability * 100,
            2
        ),
        "risk_level": risk_level,
        "threshold": round(
            THRESHOLD,
            6
        )
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    sample = {
        "Time": 406.0,

        "V1": -1.359807,
        "V2": -0.072781,
        "V3": 2.536347,
        "V4": 1.378155,
        "V5": -0.338321,
        "V6": 0.462388,
        "V7": 0.239599,
        "V8": 0.098698,
        "V9": 0.363787,
        "V10": 0.090794,
        "V11": -0.551600,
        "V12": -0.617801,
        "V13": -0.991390,
        "V14": -0.311169,
        "V15": 1.468177,
        "V16": -0.470400,
        "V17": 0.207971,
        "V18": 0.025791,
        "V19": 0.403993,
        "V20": 0.251412,
        "V21": -0.018307,
        "V22": 0.277838,
        "V23": -0.110474,
        "V24": 0.066928,
        "V25": 0.128539,
        "V26": -0.189115,
        "V27": 0.133558,
        "V28": -0.021053,

        "Amount": 149.62
    }

    result = predict_transaction(sample)

    print("=" * 70)
    print("FRAUD TRANSACTION DETECTOR")
    print("=" * 70)

    for key, value in result.items():
        print(f"{key}: {value}")