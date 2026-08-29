from pathlib import Path
import time
import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    average_precision_score,
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score
)


# ============================================================
# CONFIG
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = ROOT_DIR / "models"

RANDOM_STATE = 42


# ============================================================
# LOAD PROCESSED DATA
# ============================================================

print("=" * 70)
print("LOADING PROCESSED DATA")
print("=" * 70)

X_train = pd.read_csv(MODEL_DIR / "X_train.csv")
X_test = pd.read_csv(MODEL_DIR / "X_test.csv")

y_train = pd.read_csv(MODEL_DIR / "y_train.csv").squeeze("columns")
y_test = pd.read_csv(MODEL_DIR / "y_test.csv").squeeze("columns")

print(f"X_train: {X_train.shape}")
print(f"X_test : {X_test.shape}")


# ============================================================
# MODELS
# ============================================================

models = {

    "Logistic Regression": LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=RANDOM_STATE
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_leaf=2,
        class_weight="balanced_subsample",
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

    start_time = time.time()

    model.fit(X_train, y_train)

    training_time = time.time() - start_time

    # Predictions
    y_pred = model.predict(X_test)

    # Probability of fraud
    y_prob = model.predict_proba(X_test)[:, 1]

    # Metrics
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
        "Training Time (sec)": training_time
    })

    # ========================================================
    # OUTPUT
    # ========================================================

    print(f"\nTraining time: {training_time:.2f} sec")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=["Legitimate", "Fraud"],
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

    # Save model
    filename = (
        name.lower()
        .replace(" ", "_")
        + ".pkl"
    )

    joblib.dump(
        model,
        MODEL_DIR / filename
    )

    print(f"\nSaved: models/{filename}")


# ============================================================
# MODEL COMPARISON
# ============================================================

results_df = (
    pd.DataFrame(results)
    .sort_values(
        by="PR-AUC",
        ascending=False
    )
)

print("\n" + "=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# ============================================================
# SAVE RESULTS
# ============================================================

results_df.to_csv(
    MODEL_DIR / "baseline_results.csv",
    index=False
)

print("\n✓ Results saved to:")
print("models/baseline_results.csv")

print("\nBASELINE TRAINING COMPLETED.")