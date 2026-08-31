import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load test data
X_test = joblib.load("dataset/processed/X_test.pkl")
y_test = joblib.load("dataset/processed/y_test.pkl")

# Load models
decision_tree = joblib.load("ml/models/decision_tree.pkl")
random_forest = joblib.load("ml/models/random_forest.pkl")
xgboost = joblib.load("ml/models/xgboost.pkl")

models = {
    "Decision Tree": decision_tree,
    "Random Forest": random_forest,
    "XGBoost": xgboost
}

print("="*80)
print("MODEL COMPARISON")
print("="*80)

for name, model in models.items():

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted")
    recall = recall_score(y_test, y_pred, average="weighted")
    f1 = f1_score(y_test, y_pred, average="weighted")

    print(f"\n{name}")
    print("-"*40)
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")