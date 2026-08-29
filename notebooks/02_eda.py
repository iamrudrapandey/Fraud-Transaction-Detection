# notebooks/02_eda.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# CONFIGURATION
# =========================
DATA_PATH = "dataset/creditcard.csv"

sns.set_theme(style="whitegrid")
pd.set_option("display.max_columns", None)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(DATA_PATH)

# =========================
# BASIC DATA PROFILE
# =========================
print("=" * 60)
print("DATASET PROFILE")
print("=" * 60)

print(f"Shape       : {df.shape}")
print(f"Memory      : {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print(f"Duplicates  : {df.duplicated().sum():,}")
print(f"Missing     : {df.isna().sum().sum():,}")

# =========================
# TARGET ANALYSIS
# =========================
target_counts = df["Class"].value_counts()
target_percent = df["Class"].value_counts(normalize=True) * 100

print("\n" + "=" * 60)
print("CLASS DISTRIBUTION")
print("=" * 60)

print(
    pd.DataFrame({
        "Count": target_counts,
        "Percentage": target_percent.round(4)
    })
)

# =========================
# NUMERIC SUMMARY
# =========================
print("\n" + "=" * 60)
print("NUMERIC SUMMARY")
print("=" * 60)

print(df.describe().T.round(4))

# =========================
# FRAUD STATISTICS
# =========================
fraud_df = df[df["Class"] == 1]
normal_df = df[df["Class"] == 0]

print("\n" + "=" * 60)
print("FRAUD TRANSACTION STATISTICS")
print("=" * 60)

print(f"Fraud transactions : {len(fraud_df):,}")
print(f"Fraud rate         : {len(fraud_df) / len(df) * 100:.4f}%")
print(f"Average fraud amt  : {fraud_df['Amount'].mean():.2f}")
print(f"Median fraud amt   : {fraud_df['Amount'].median():.2f}")
print(f"Maximum fraud amt  : {fraud_df['Amount'].max():.2f}")

# =========================
# 1. CLASS DISTRIBUTION
# =========================
plt.figure(figsize=(7, 5))

sns.countplot(
    data=df,
    x="Class",
    hue="Class",
    legend=False
)

plt.title("Transaction Class Distribution")
plt.xlabel("Class (0 = Legitimate, 1 = Fraud)")
plt.ylabel("Transaction Count")
plt.tight_layout()
plt.show()

# =========================
# 2. LOG-SCALE CLASS DISTRIBUTION
# =========================
plt.figure(figsize=(7, 5))

sns.countplot(
    data=df,
    x="Class",
    hue="Class",
    legend=False
)

plt.yscale("log")
plt.title("Transaction Distribution (Log Scale)")
plt.xlabel("Class")
plt.ylabel("Transaction Count - Log Scale")
plt.tight_layout()
plt.show()

# =========================
# 3. AMOUNT DISTRIBUTION
# =========================
plt.figure(figsize=(9, 5))

sns.histplot(
    data=df,
    x="Amount",
    bins=100,
    log_scale=True
)

plt.title("Transaction Amount Distribution")
plt.xlabel("Amount - Log Scale")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# =========================
# 4. AMOUNT: FRAUD VS NORMAL
# =========================
plt.figure(figsize=(9, 5))

sns.boxplot(
    data=df,
    x="Class",
    y="Amount",
    showfliers=False
)

plt.title("Transaction Amount: Fraud vs Legitimate")
plt.xlabel("Class")
plt.ylabel("Amount")
plt.tight_layout()
plt.show()

# =========================
# 5. TIME DISTRIBUTION
# =========================
plt.figure(figsize=(10, 5))

sns.histplot(
    data=df,
    x="Time",
    hue="Class",
    bins=100,
    element="step",
    stat="density",
    common_norm=False
)

plt.title("Transaction Time Distribution")
plt.xlabel("Time")
plt.ylabel("Density")
plt.tight_layout()
plt.show()

# =========================
# 6. FEATURE CORRELATION
# =========================
correlation = df.corr(numeric_only=True)

plt.figure(figsize=(16, 12))

sns.heatmap(
    correlation,
    cmap="coolwarm",
    center=0,
    linewidths=0.1,
    cbar=True
)

plt.title("Feature Correlation Matrix")
plt.tight_layout()
plt.show()

# =========================
# 7. CORRELATION WITH TARGET
# =========================
target_corr = (
    correlation["Class"]
    .drop("Class")
    .sort_values()
)

plt.figure(figsize=(10, 8))

target_corr.plot(kind="barh")

plt.title("Feature Correlation with Fraud Class")
plt.xlabel("Correlation")
plt.ylabel("Features")
plt.tight_layout()
plt.show()

# =========================
# 8. TOP FEATURES BY ABSOLUTE
#    CORRELATION
# =========================
top_features = (
    target_corr.abs()
    .sort_values(ascending=False)
    .head(10)
    .index
)

print("\n" + "=" * 60)
print("TOP 10 FEATURES BY ABSOLUTE TARGET CORRELATION")
print("=" * 60)

print(target_corr.loc[top_features].sort_values(ascending=False))

# =========================
# 9. FRAUD AMOUNT SUMMARY
# =========================
amount_summary = (
    df.groupby("Class")["Amount"]
    .agg(
        Count="count",
        Mean="mean",
        Median="median",
        Std="std",
        Min="min",
        Max="max"
    )
    .round(2)
)

print("\n" + "=" * 60)
print("AMOUNT SUMMARY BY CLASS")
print("=" * 60)

print(amount_summary)

# =========================
# 10. DATA QUALITY REPORT
# =========================
quality_report = pd.DataFrame({
    "dtype": df.dtypes,
    "missing": df.isna().sum(),
    "unique": df.nunique(),
    "missing_%": (df.isna().mean() * 100).round(4)
})

print("\n" + "=" * 60)
print("DATA QUALITY REPORT")
print("=" * 60)

print(quality_report)

print("\nEDA COMPLETED SUCCESSFULLY.")