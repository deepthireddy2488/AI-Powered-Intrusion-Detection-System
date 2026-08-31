import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

print("Loading cleaned dataset...")

# Load cleaned dataset
df = pd.read_csv("dataset/processed/cleaned_dataset.csv")

# Separate features and target
X = df.drop("Label", axis=1)
y = df["Label"]

# Save feature names
joblib.dump(list(X.columns), "ml/models/features.pkl")

# Encode attack labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Save label encoder
joblib.dump(label_encoder, "ml/models/label_encoder.pkl")

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training Samples :", len(X_train))
print("Testing Samples  :", len(X_test))

# Save split datasets
joblib.dump(X_train, "dataset/processed/X_train.pkl")
joblib.dump(X_test, "dataset/processed/X_test.pkl")
joblib.dump(y_train, "dataset/processed/y_train.pkl")
joblib.dump(y_test, "dataset/processed/y_test.pkl")

print("\nData preparation completed successfully!")