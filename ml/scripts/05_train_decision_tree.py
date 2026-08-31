import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

print("Loading training and testing data...")

# Load datasets
X_train = joblib.load("dataset/processed/X_train.pkl")
X_test = joblib.load("dataset/processed/X_test.pkl")
y_train = joblib.load("dataset/processed/y_train.pkl")
y_test = joblib.load("dataset/processed/y_test.pkl")

print("Training Decision Tree Model...")

# Create model
model = DecisionTreeClassifier(
    random_state=42
)

# Train model
model.fit(X_train, y_train)

print("Model training completed!")

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {accuracy * 100:.2f}%")

# Save model
joblib.dump(model, "ml/models/decision_tree.pkl")

print("\nDecision Tree model saved successfully!")