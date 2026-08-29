from pathlib import Path
import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    precision_recall_curve,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report
)


# ============================================================
# CONFIG
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = ROOT_DIR / "models"

MODEL_PATH = MODEL_DIR / "optimized_xgboost.pkl"

# Minimum acceptable recall for fraud detection
MIN_RECALL = 0.80


# ============================================================
# LOAD
# ============================================================

print("=" * 70)
print("FINAL THRESHOLD OPTIMIZATION")
print("=" * 70)

model = joblib.load(MODEL_PATH)

X_test = pd.read_csv(
    MODEL_DIR / "X_test.csv"
)

y_test = pd.read_csv(
    MODEL_DIR / "y_test.csv"
).squeeze("columns")


# ============================================================
# PREDICT PROBABILITIES
# ============================================================

y_prob = model.predict_proba(X_test)[:, 1]


# ============================================================
# GLOBAL METRICS
# ============================================================

roc_auc = roc_auc_score(
    y_test,
    y_prob
)

pr_auc = average_precision_score(
    y_test,
    y_prob
)

print(f"\nROC-AUC : {roc_auc:.4f}")
print(f"PR-AUC  : {pr_auc:.4f}")


# ============================================================
# PRECISION / RECALL CURVE
# ============================================================

precision, recall, thresholds = precision_recall_curve(
    y_test,
    y_prob
)

f1 = (
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

best_idx = np.argmax(f1)

best_threshold = thresholds[best_idx]

print("\n" + "=" * 70)
print("BEST F1 THRESHOLD")
print("=" * 70)

print(f"Threshold : {best_threshold:.6f}")
print(f"Precision : {precision[best_idx]:.4f}")
print(f"Recall    : {recall[best_idx]:.4f}")
print(f"F1 Score  : {f1[best_idx]:.4f}")


# ============================================================
# BEST THRESHOLD WITH RECALL >= 80%
# ============================================================

valid = recall[:-1] >= MIN_RECALL

if valid.any():

    valid_indices = np.where(valid)[0]

    best_recall_idx = valid_indices[
        np.argmax(
            f1[valid_indices]
        )
    ]

    recall_threshold = thresholds[
        best_recall_idx
    ]

    print("\n" + "=" * 70)
    print(f"BEST F1 WITH RECALL >= {MIN_RECALL:.0%}")
    print("=" * 70)

    print(
        f"Threshold : {recall_threshold:.6f}"
    )

    print(
        f"Precision : "
        f"{precision[best_recall_idx]:.4f}"
    )

    print(
        f"Recall    : "
        f"{recall[best_recall_idx]:.4f}"
    )

    print(
        f"F1 Score  : "
        f"{f1[best_recall_idx]:.4f}"
    )

else:

    recall_threshold = best_threshold

    print(
        "\nNo threshold achieved "
        f"{MIN_RECALL:.0%} recall."
    )


# ============================================================
# THRESHOLD EVALUATION FUNCTION
# ============================================================

def evaluate_threshold(threshold):

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

    f = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    tn, fp, fn, tp = confusion_matrix(
        y_test,
        predictions
    ).ravel()

    return {
        "Threshold": threshold,
        "Precision": p,
        "Recall": r,
        "F1": f,
        "True_Negative": tn,
        "False_Positive": fp,
        "False_Negative": fn,
        "True_Positive": tp
    }


# ============================================================
# COMPARE IMPORTANT THRESHOLDS
# ============================================================

thresholds_to_test = [
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
    0.70,
    0.80,
    0.90,
    float(best_threshold),
    float(recall_threshold)
]

thresholds_to_test = sorted(
    set(
        round(x, 6)
        for x in thresholds_to_test
    )
)

comparison = pd.DataFrame(
    [
        evaluate_threshold(t)
        for t in thresholds_to_test
    ]
)

print("\n" + "=" * 70)
print("THRESHOLD COMPARISON")
print("=" * 70)

print(
    comparison.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# ============================================================
# FINAL MODEL THRESHOLD
# ============================================================

final_threshold = recall_threshold

final_predictions = (
    y_prob >= final_threshold
).astype(int)

print("\n" + "=" * 70)
print("FINAL MODEL PERFORMANCE")
print("=" * 70)

print(
    classification_report(
        y_test,
        final_predictions,
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
        final_predictions
    )
)


# ============================================================
# SAVE
# ============================================================

comparison.to_csv(
    MODEL_DIR / "final_threshold_comparison.csv",
    index=False
)

joblib.dump(
    {
        "threshold": float(final_threshold),
        "roc_auc": float(roc_auc),
        "pr_auc": float(pr_auc)
    },
    MODEL_DIR / "final_threshold.pkl"
)


print("\n" + "=" * 70)
print("FINAL THRESHOLD SAVED")
print("=" * 70)

print(
    f"Threshold: {final_threshold:.6f}"
)

print(
    "Saved: models/final_threshold.pkl"
)

print(
    "Saved: models/final_threshold_comparison.csv"
)
