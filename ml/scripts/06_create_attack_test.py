import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

input_file = BASE_DIR / "dataset" / "processed" / "cleaned_dataset.csv"
output_file = BASE_DIR / "ml" / "models" / "attack_test.csv"

df = pd.read_csv(input_file)

# Select only attack records
attack_df = df[df["Label"] != "BENIGN"]

# Take first 10 attack records
attack_df = attack_df.head(10)

# Remove Label because the prediction API does not need it
if "Label" in attack_df.columns:
    attack_df = attack_df.drop(columns=["Label"])

attack_df.to_csv(output_file, index=False)

print("Attack test file created!")
print(output_file)
print("Rows:", len(attack_df))