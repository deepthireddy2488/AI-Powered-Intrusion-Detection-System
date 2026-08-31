import pandas as pd

# Load merged dataset
df = pd.read_csv("dataset/processed/merged_dataset.csv")

print("=" * 60)
print("DATASET SHAPE")
print("=" * 60)
print(df.shape)

print("\n")

print("=" * 60)
print("FIRST 5 ROWS")
print("=" * 60)
print(df.head())

print("\n")

print("=" * 60)
print("COLUMN NAMES")
print("=" * 60)
print(df.columns.tolist())

print("\n")

print("=" * 60)
print("DATASET INFORMATION")
print("=" * 60)
print(df.info())

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

print(df.isnull().sum())

print("\n" + "=" * 60)
print("DUPLICATE ROWS")
print("=" * 60)

print(df.duplicated().sum())

print("\n" + "=" * 60)
print("ATTACK LABEL DISTRIBUTION")
print("=" * 60)

print(df[" Label"].value_counts())