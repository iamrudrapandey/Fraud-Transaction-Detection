# src/01_preprocess.py

from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler


# ============================================================
# CONFIG
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = ROOT_DIR / "dataset" / "creditcard.csv"
MODEL_DIR = ROOT_DIR / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("LOADING DATASET")
print("=" * 70)

df = pd.read_csv(DATA_PATH)

print(f"Dataset shape: {df.shape}")


# ============================================================
# DATA QUALITY
# ============================================================

print("\n" + "=" * 70)
print("DATA QUALITY")
print("=" * 70)

missing_values = df.isna().sum().sum()
duplicates = df.duplicated().sum()

print(f"Missing values : {missing_values:,}")
print(f"Duplicate rows : {duplicates:,}")


# ============================================================
# REMOVE DUPLICATES
# ============================================================

if duplicates > 0:
    df = df.drop_duplicates().reset_index(drop=True)

print(f"\nShape after duplicate removal: {df.shape}")


# ============================================================
# FEATURES / TARGET
# ============================================================

X = df.drop(columns=["Class"])
y = df["Class"]


# ============================================================
# TRAIN / TEST SPLIT
# IMPORTANT:
# Stratification preserves the fraud ratio.
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42
)


# ============================================================
# SCALE AMOUNT
#
# RobustScaler is preferred because transaction amounts
# can contain extreme values/outliers.
#
# FIT ONLY ON TRAINING DATA -> prevents data leakage.
# ============================================================

scaler = RobustScaler()

X_train = X_train.copy()
X_test = X_test.copy()

X_train["Amount"] = scaler.fit_transform(
    X_train[["Amount"]]
)

X_test["Amount"] = scaler.transform(
    X_test[["Amount"]]
)


# ============================================================
# OPTIONAL TIME TRANSFORMATION
#
# Convert Time into cyclical hour-like features.
# The dataset Time is seconds elapsed from the first transaction.
# ============================================================

SECONDS_PER_DAY = 24 * 60 * 60

for data in (X_train, X_test):

    time_seconds = data["Time"] % SECONDS_PER_DAY

    data["Time_sin"] = __import__("numpy").sin(
        2 * __import__("numpy").pi * time_seconds / SECONDS_PER_DAY
    )

    data["Time_cos"] = __import__("numpy").cos(
        2 * __import__("numpy").pi * time_seconds / SECONDS_PER_DAY
    )


# Drop original Time after creating cyclical representation

X_train.drop(columns=["Time"], inplace=True)
X_test.drop(columns=["Time"], inplace=True)


# ============================================================
# SAVE PROCESSED DATA
# ============================================================

X_train.to_csv(
    MODEL_DIR / "X_train.csv",
    index=False
)

X_test.to_csv(
    MODEL_DIR / "X_test.csv",
    index=False
)

y_train.to_csv(
    MODEL_DIR / "y_train.csv",
    index=False
)

y_test.to_csv(
    MODEL_DIR / "y_test.csv",
    index=False
)


# ============================================================
# SAVE SCALER
# ============================================================

joblib.dump(
    scaler,
    MODEL_DIR / "robust_scaler.pkl"
)


# ============================================================
# REPORT
# ============================================================

print("\n" + "=" * 70)
print("PREPROCESSING COMPLETED")
print("=" * 70)

print(f"Training samples : {len(X_train):,}")
print(f"Testing samples  : {len(X_test):,}")

print("\nTraining class distribution:")
print(y_train.value_counts())

print("\nTesting class distribution:")
print(y_test.value_counts())

print("\nFraud percentage:")

print(
    f"Train: {y_train.mean() * 100:.4f}%"
)

print(
    f"Test : {y_test.mean() * 100:.4f}%"
)

print("\nProcessed feature count:")
print(X_train.shape[1])

print("\nSaved files:")
print("✓ X_train.csv")
print("✓ X_test.csv")
print("✓ y_train.csv")
print("✓ y_test.csv")
print("✓ robust_scaler.pkl")