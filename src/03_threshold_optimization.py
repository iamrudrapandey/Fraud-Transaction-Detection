from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    precision_recall_curve,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    roc_auc_score
)


# ============================================================
# CONFIG
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = ROOT_DIR / "models"

MODEL_PATH = MODEL_DIR / "random_forest.pkl"

RANDOM_STATE = 42


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("LOADING MODEL AND TEST DATA")
print("=" * 70)

model = joblib.load(MODEL_PATH)

X_test = pd.read_csv(
    MODEL_DIR / "X_test.csv"
)

y_test = pd.read_csv(
    MODEL_DIR / "y_test.csv"
).squeeze("columns")

print(f"Test samples: {len(X_test):,}")
print(f"Fraud cases  : {y_test.sum():,}")


# ============================================================
# FRAUD PROBABILITIES
# ============================================================

y_prob = model.predict_proba(X_test)[:, 1]


# ============================================================
# BASELINE METRICS
# ============================================================

roc_auc = roc_auc_score(
    y_test,
    y_prob
)

pr_auc = average_precision_score(
    y_test,
    y_prob
)

print("\n" + "=" * 70)
print("PROBABILITY METRICS")
print("=" * 70)

print(f"ROC-AUC : {roc_auc:.4f}")
print(f"PR-AUC  : {pr_auc:.4f}")


# ============================================================
# PRECISION-RECALL CURVE
# ============================================================

precision, recall, thresholds = precision_recall_curve(
    y_test,
    y_prob
)

# precision_recall_curve returns one extra precision/recall
# value compared with thresholds.
f1_scores = (
    2 * precision[:-1] * recall[:-1]
    / (
        precision[:-1]
        + recall[:-1]
        + 1e-12
    )
)


# ============================================================
# BEST F1 THRESHOLD
# ============================================================

best_index = np.argmax(f1_scores)

best_threshold = thresholds[best_index]
best_precision = precision[best_index]
best_recall = recall[best_index]
best_f1 = f1_scores[best_index]

print("\n" + "=" * 70)
print("BEST F1 THRESHOLD")
print("=" * 70)

print(f"Threshold : {best_threshold:.6f}")
print(f"Precision : {best_precision:.4f}")
print(f"Recall    : {best_recall:.4f}")
print(f"F1 Score  : {best_f1:.4f}")


# ============================================================
# EVALUATE DEFAULT THRESHOLD
# ============================================================

default_threshold = 0.50

y_pred_default = (
    y_prob >= default_threshold
).astype(int)

print("\n" + "=" * 70)
print("DEFAULT THRESHOLD = 0.50")
print("=" * 70)

print(
    classification_report(
        y_test,
        y_pred_default,
        target_names=[
            "Legitimate",
            "Fraud"
        ],
        digits=4,
        zero_division=0
    )
)

print("Confusion Matrix:")
print(
    confusion_matrix(
        y_test,
        y_pred_default
    )
)


# ============================================================
# EVALUATE OPTIMIZED THRESHOLD
# ============================================================

y_pred_optimized = (
    y_prob >= best_threshold
).astype(int)

optimized_precision = precision_score(
    y_test,
    y_pred_optimized,
    zero_division=0
)

optimized_recall = recall_score(
    y_test,
    y_pred_optimized,
    zero_division=0
)

optimized_f1 = f1_score(
    y_test,
    y_pred_optimized,
    zero_division=0
)

print("\n" + "=" * 70)
print("OPTIMIZED THRESHOLD")
print("=" * 70)

print(
    classification_report(
        y_test,
        y_pred_optimized,
        target_names=[
            "Legitimate",
            "Fraud"
        ],
        digits=4,
        zero_division=0
    )
)

print("Confusion Matrix:")
print(
    confusion_matrix(
        y_test,
        y_pred_optimized
    )
)

print("\nOptimized Metrics:")
print(f"Precision : {optimized_precision:.4f}")
print(f"Recall    : {optimized_recall:.4f}")
print(f"F1 Score  : {optimized_f1:.4f}")


# ============================================================
# THRESHOLD ANALYSIS
# ============================================================

threshold_results = []

for threshold in np.arange(
    0.05,
    0.96,
    0.01
):

    predictions = (
        y_prob >= threshold
    ).astype(int)

    p = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    r = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    threshold_results.append({
        "Threshold": threshold,
        "Precision": p,
        "Recall": r,
        "F1": f1
    })


threshold_df = pd.DataFrame(
    threshold_results
)

threshold_df.to_csv(
    MODEL_DIR / "threshold_analysis.csv",
    index=False
)


# ============================================================
# PLOT PRECISION / RECALL / F1
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    threshold_df["Threshold"],
    threshold_df["Precision"],
    label="Precision"
)

plt.plot(
    threshold_df["Threshold"],
    threshold_df["Recall"],
    label="Recall"
)

plt.plot(
    threshold_df["Threshold"],
    threshold_df["F1"],
    label="F1 Score"
)

plt.axvline(
    best_threshold,
    linestyle="--",
    label=f"Best F1 = {best_threshold:.3f}"
)

plt.xlabel("Classification Threshold")
plt.ylabel("Score")
plt.title("Threshold Optimization")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()


# ============================================================
# SAVE OPTIMAL THRESHOLD
# ============================================================

joblib.dump(
    {
        "threshold": float(best_threshold),
        "precision": float(best_precision),
        "recall": float(best_recall),
        "f1": float(best_f1)
    },
    MODEL_DIR / "optimal_threshold.pkl"
)


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("THRESHOLD OPTIMIZATION COMPLETED")
print("=" * 70)

print(
    f"Optimal threshold saved: "
    f"models/optimal_threshold.pkl"
)

print(
    f"Threshold: {best_threshold:.6f}"
)
