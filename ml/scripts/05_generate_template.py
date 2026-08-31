import pandas as pd
import joblib
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Models folder
MODEL_DIR = BASE_DIR / "ml" / "models"

# Load trained feature names
features = joblib.load(MODEL_DIR / "features.pkl")

# Create 5 sample rows
data = []

for i in range(5):
    row = {}

    for feature in features:
        row[feature] = 0

    data.append(row)

# Create DataFrame
df = pd.DataFrame(data, columns=features)

# Save sample CSV
output_path = MODEL_DIR / "prediction_sample.csv"

df.to_csv(output_path, index=False)

print("Sample prediction file created successfully!")
print(output_path)
print("Rows:", len(df))
print("Columns:", len(df.columns))