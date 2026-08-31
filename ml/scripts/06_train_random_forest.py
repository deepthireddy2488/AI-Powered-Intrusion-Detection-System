import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

print("Loading training and testing data...")

# Load datasets
X_train = joblib.load("dataset/processed/X_train.pkl")
X_test = joblib.load("dataset/processed/X_test.pkl")
y_train = joblib.load("dataset/processed/y_train.pkl")
y_test = joblib.load("dataset/processed/y_test.pkl")

print("Training Random Forest Model...")

# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
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
joblib.dump(model, "ml/models/random_forest.pkl")

print("\nRandom Forest model saved successfully!")