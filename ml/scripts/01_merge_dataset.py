import os
import glob
import pandas as pd

# Folder paths
RAW_DATA_PATH = os.path.join("dataset", "raw")
PROCESSED_DATA_PATH = os.path.join("dataset", "processed")
OUTPUT_FILE = os.path.join(PROCESSED_DATA_PATH, "merged_dataset.csv")

# Find all CSV files except Week_filtered.csv
csv_files = [
    file for file in glob.glob(os.path.join(RAW_DATA_PATH, "*.csv"))
    if "Week_filtered.csv" not in os.path.basename(file)
]

print(f"Found {len(csv_files)} CSV files.")

# Read and merge all datasets
dataframes = []

for file in csv_files:
    print(f"Reading: {os.path.basename(file)}")
    df = pd.read_csv(file)
    dataframes.append(df)

merged_df = pd.concat(dataframes, ignore_index=True)

# Save merged dataset
merged_df.to_csv(OUTPUT_FILE, index=False)

print("\nDataset merged successfully!")
print(f"Rows: {merged_df.shape[0]}")
print(f"Columns: {merged_df.shape[1]}")
print(f"Saved to: {OUTPUT_FILE}")