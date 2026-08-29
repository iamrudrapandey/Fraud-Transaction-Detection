from pathlib import Path
import time
import joblib
import pandas as pd
import numpy as np

from imblearn.over_sampling import SMOTE

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    classification_report,
    confusion_matrix
)

from xgboost import XGBClassifier


# ============================================================
# CONFIG
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = ROOT_DIR / "models"

RANDOM_STATE = 42


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("LOADING DATA")
print("=" * 70)

X_train = pd.read_csv(MODEL_DIR / "X_train.csv")
X_test = pd.read_csv(MODEL_DIR / "X_test.csv")

y_train = pd.read_csv(
    MODEL_DIR / "y_train.csv"
).squeeze("columns")

y_test = pd.read_csv(
    MODEL_DIR / "y_test.csv"
).squeeze("columns")

print(f"Original training data: {X_train.shape}")
print(f"Test data              : {X_test.shape}")

print("\nOriginal class distribution:")
print(y_train.value_counts())


# ============================================================
# SMOTE
# ============================================================

print("\n" + "=" * 70)
print("APPLYING SMOTE")
print("=" * 70)

smote = SMOTE(
    sampling_strategy=0.25,
    random_state=RANDOM_STATE,
    k_neighbors=5
)

X_train_smote, y_train_smote = smote.fit_resample(
    X_train,
    y_train
)

print("After SMOTE:")
print(
    pd.Series(y_train_smote).value_counts()
)

print(
    f"\nNew training shape: {X_train_smote.shape}"
)


# ============================================================
# MODELS
# ============================================================

models = {

    "SMOTE Random Forest": RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_leaf=2,
        class_weight=None,
        n_jobs=-1,
        random_state=RANDOM_STATE
    ),

    "XGBoost": XGBClassifier(
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.85,
        colsample_bytree=0.85,
        min_child_weight=3,
        gamma=0,
        reg_alpha=0.1,
        reg_lambda=1.0,
        objective="binary:logistic",
        eval_metric="logloss",
        tree_method="hist",
        n_jobs=-1,
        random_state=RANDOM_STATE
    )
}


# ============================================================
# TRAIN + EVALUATE
# ============================================================

results = []

for name, model in models.items():

    print("\n" + "=" * 70)
    print(f"TRAINING: {name}")
    print("=" * 70)

    start = time.time()

    model.fit(
        X_train_smote,
        y_train_smote
    )

    training_time = time.time() - start

    # --------------------------------------------------------
    # Predictions
    # --------------------------------------------------------

    y_prob = model.predict_proba(
        X_test
    )[:, 1]

    # Default threshold
    y_pred = (
        y_prob >= 0.50
    ).astype(int)

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        y_prob
    )

    pr_auc = average_precision_score(
        y_test,
        y_prob
    )

    results.append({
        "Model": name,
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
        "ROC-AUC": roc_auc,
        "PR-AUC": pr_auc,
        "Training Time": training_time
    })

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print(f"\nTraining time: {training_time:.2f} seconds")

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            y_pred,
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
            y_pred
        )
    )

    print(f"\nPrecision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")
    print(f"ROC-AUC   : {roc_auc:.4f}")
    print(f"PR-AUC    : {pr_auc:.4f}")

    # --------------------------------------------------------
    # Save model
    # --------------------------------------------------------

    filename = (
        name.lower()
        .replace(" ", "_")
        + ".pkl"
    )

    joblib.dump(
        model,
        MODEL_DIR / filename
    )

    print(
        f"\nSaved: models/{filename}"
    )


# ============================================================
# COMPARISON
# ============================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="PR-AUC",
    ascending=False
)

print("\n" + "=" * 70)
print("ADVANCED MODEL COMPARISON")
print("=" * 70)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)

results_df.to_csv(
    MODEL_DIR / "advanced_results.csv",
    index=False
)

print(
    "\n✓ Saved: models/advanced_results.csv"
)

print("\nADVANCED MODEL TRAINING COMPLETED.")