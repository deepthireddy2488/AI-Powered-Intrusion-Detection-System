import joblib
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

print("Loading training and testing data...")

# Load datasets
X_train = joblib.load("dataset/processed/X_train.pkl")
X_test = joblib.load("dataset/processed/X_test.pkl")
y_train = joblib.load("dataset/processed/y_train.pkl")
y_test = joblib.load("dataset/processed/y_test.pkl")

print("Training XGBoost Model...")

# Create model
model = XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    random_state=42,
    eval_metric="mlogloss"
)

# Train model
model.fit(X_train, y_train)

print("Model training completed!")

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "ml/models/xgboost.pkl")

print("\nXGBoost model saved successfully!")