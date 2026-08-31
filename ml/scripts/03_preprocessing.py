import pandas as pd
import numpy as np


# ============================================================
# LOAD DATASET
# ============================================================

print("===================================")
print(" AI IDS DATA PREPROCESSING")
print("===================================")

print("\nLoading dataset...")

input_path = "dataset/processed/merged_dataset.csv"
output_path = "dataset/processed/cleaned_dataset.csv"


df = pd.read_csv(input_path)


print(f"Original Shape: {df.shape}")


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

print("\nCleaning column names...")

df.columns = df.columns.str.strip()


print("Column names cleaned.")


# ============================================================
# REMOVE DUPLICATE ROWS
# ============================================================

print("\nChecking duplicate rows...")

duplicates_before = df.duplicated().sum()

print(
    f"Duplicate rows before: "
    f"{duplicates_before}"
)


df = df.drop_duplicates()


duplicates_after = df.duplicated().sum()

print(
    f"Duplicate rows after: "
    f"{duplicates_after}"
)


# ============================================================
# REPLACE INFINITY VALUES
# ============================================================

print("\nChecking infinity values...")

infinity_count = np.isinf(
    df.select_dtypes(include=np.number)
).sum().sum()


print(
    f"Infinity values found: "
    f"{infinity_count}"
)


df.replace(
    [np.inf, -np.inf],
    np.nan,
    inplace=True
)


# ============================================================
# CHECK MISSING VALUES
# ============================================================

print("\nChecking missing values...")

missing_before = df.isnull().sum().sum()

print(
    f"Missing values before: "
    f"{missing_before}"
)


# ============================================================
# REMOVE ROWS WITH MISSING VALUES
# ============================================================

df.dropna(
    inplace=True
)


missing_after = df.isnull().sum().sum()

print(
    f"Missing values after: "
    f"{missing_after}"
)


# ============================================================
# FINAL DATASET INFORMATION
# ============================================================

print("\n===================================")
print(" PREPROCESSING COMPLETED")
print("===================================")

print(
    f"Final Shape: {df.shape}"
)

print(
    f"Final Columns: {len(df.columns)}"
)


# ============================================================
# SAVE CLEANED DATASET
# ============================================================

df.to_csv(
    output_path,
    index=False
)


print(
    f"Saved to: {output_path}"
)

print("===================================")