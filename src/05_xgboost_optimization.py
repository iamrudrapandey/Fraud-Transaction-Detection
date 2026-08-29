from pathlib import Path
import time
import joblib
import optuna
import pandas as pd
import numpy as np

from xgboost import XGBClassifier

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# CONFIG
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = ROOT_DIR / "models"

RANDOM_STATE = 42
N_TRIALS = 30


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


# ============================================================
# XGBOOST CLASS WEIGHT
# ============================================================

negative = (y_train == 0).sum()
positive = (y_train == 1).sum()

scale_pos_weight = negative / positive

print(f"Negative samples : {negative:,}")
print(f"Positive samples : {positive:,}")
print(f"Scale pos weight : {scale_pos_weight:.2f}")


# ============================================================
# OPTUNA OBJECTIVE
# ============================================================

def objective(trial):

    params = {
        "n_estimators": trial.suggest_int(
            "n_estimators",
            200,
            800,
            step=100
        ),

        "max_depth": trial.suggest_int(
            "max_depth",
            3,
            10
        ),

        "learning_rate": trial.suggest_float(
            "learning_rate",
            0.01,
            0.15,
            log=True
        ),

        "min_child_weight": trial.suggest_int(
            "min_child_weight",
            1,
            10
        ),

        "subsample": trial.suggest_float(
            "subsample",
            0.7,
            1.0
        ),

        "colsample_bytree": trial.suggest_float(
            "colsample_bytree",
            0.7,
            1.0
        ),

        "gamma": trial.suggest_float(
            "gamma",
            0,
            5
        ),

        "reg_alpha": trial.suggest_float(
            "reg_alpha",
            1e-4,
            10,
            log=True
        ),

        "reg_lambda": trial.suggest_float(
            "reg_lambda",
            0.1,
            10,
            log=True
        ),

        "objective": "binary:logistic",
        "eval_metric": "aucpr",
        "tree_method": "hist",
        "n_jobs": -1,
        "random_state": RANDOM_STATE,

        # Handle imbalance without modifying validation data
        "scale_pos_weight": scale_pos_weight
    }

    model = XGBClassifier(**params)

    cv = StratifiedKFold(
        n_splits=3,
        shuffle=True,
        random_state=RANDOM_STATE
    )

    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring="average_precision",
        n_jobs=1
    )

    return scores.mean()


# ============================================================
# OPTIMIZATION
# ============================================================

print("\n" + "=" * 70)
print("STARTING HYPERPARAMETER OPTIMIZATION")
print("=" * 70)

start_time = time.time()

study = optuna.create_study(
    direction="maximize",
    study_name="fraud_xgboost_optimization"
)

study.optimize(
    objective,
    n_trials=N_TRIALS,
    show_progress_bar=True
)

optimization_time = time.time() - start_time


# ============================================================
# BEST PARAMETERS
# ============================================================

print("\n" + "=" * 70)
print("BEST PARAMETERS")
print("=" * 70)

print(
    f"Best CV PR-AUC: "
    f"{study.best_value:.6f}"
)

for parameter, value in study.best_params.items():
    print(f"{parameter}: {value}")


# ============================================================
# TRAIN FINAL MODEL
# ============================================================

print("\n" + "=" * 70)
print("TRAINING OPTIMIZED XGBOOST")
print("=" * 70)

best_params = study.best_params.copy()

best_params.update({
    "objective": "binary:logistic",
    "eval_metric": "aucpr",
    "tree_method": "hist",
    "n_jobs": -1,
    "random_state": RANDOM_STATE,
    "scale_pos_weight": scale_pos_weight
})

model = XGBClassifier(
    **best_params
)

model.fit(
    X_train,
    y_train
)


# ============================================================
# TEST EVALUATION
# ============================================================

y_prob = model.predict_proba(
    X_test
)[:, 1]

y_pred = (
    y_prob >= 0.50
).astype(int)


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


# ============================================================
# RESULTS
# ============================================================

print("\n" + "=" * 70)
print("OPTIMIZED XGBOOST RESULTS")
print("=" * 70)

print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC-AUC   : {roc_auc:.4f}")
print(f"PR-AUC    : {pr_auc:.4f}")

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


# ============================================================
# SAVE MODEL
# ============================================================

model_path = (
    MODEL_DIR /
    "optimized_xgboost.pkl"
)

joblib.dump(
    model,
    model_path
)


# ============================================================
# SAVE OPTUNA STUDY
# ============================================================

study.trials_dataframe().to_csv(
    MODEL_DIR /
    "optuna_trials.csv",
    index=False
)


# ============================================================
# FINAL INFO
# ============================================================

print("\n" + "=" * 70)
print("OPTIMIZATION COMPLETED")
print("=" * 70)

print(
    f"Optimization time: "
    f"{optimization_time / 60:.2f} minutes"
)

print(
    f"Model saved: {model_path}"
)

print(
    "Trials saved: "
    "models/optuna_trials.csv"
) 