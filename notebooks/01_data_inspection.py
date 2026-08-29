import pandas as pd

# Load dataset
df = pd.read_csv("dataset/creditcard.csv")

# Basic information
print("Dataset Shape:", df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nColumn Names:")
print(df.columns)

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nClass Distribution:")
print(df["Class"].value_counts())

print("\nStatistical Summary:")
print(df.describe())