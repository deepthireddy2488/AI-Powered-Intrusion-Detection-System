import joblib

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ============================================
# PATHS
# ============================================

MODEL_PATH = "ml/models/random_forest.pkl"

X_TEST_PATH = "dataset/processed/X_test.pkl"

Y_TEST_PATH = "dataset/processed/y_test.pkl"

ENCODER_PATH = "ml/models/label_encoder.pkl"


# ============================================
# LOAD MODEL
# ============================================

print()
print("========================================")
print("      AI IDS MODEL EVALUATION")
print("========================================")

print()
print("Loading Random Forest model...")

model = joblib.load(
    MODEL_PATH
)

print(
    "Model loaded successfully!"
)


# ============================================
# LOAD TEST DATA
# ============================================

print()
print("Loading test data...")

X_test = joblib.load(
    X_TEST_PATH
)

y_test = joblib.load(
    Y_TEST_PATH
)

print(
    f"Test samples: {len(X_test)}"
)

print(
    f"Test features: {X_test.shape[1]}"
)


# ============================================
# LOAD LABEL ENCODER
# ============================================

print()
print("Loading label encoder...")

label_encoder = joblib.load(
    ENCODER_PATH
)

print(
    "Label encoder loaded successfully!"
)


# ============================================
# PREDICTION
# ============================================

print()
print("Starting predictions...")

y_pred = model.predict(
    X_test
)

print(
    "Predictions completed!"
)


# ============================================
# ACCURACY
# ============================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


print()
print("========================================")
print("              ACCURACY")
print("========================================")

print(
    f"Accuracy: {accuracy:.4f}"
)

print(
    f"Accuracy Percentage: {accuracy * 100:.2f}%"
)


# ============================================
# CLASSIFICATION REPORT
# ============================================

print()
print("========================================")
print("       CLASSIFICATION REPORT")
print("========================================")

report = classification_report(

    y_test,

    y_pred,

    target_names=label_encoder.classes_,

    zero_division=0
)

print(
    report
)


# ============================================
# CONFUSION MATRIX
# ============================================

print()
print("========================================")
print("          CONFUSION MATRIX")
print("========================================")

matrix = confusion_matrix(
    y_test,
    y_pred
)

print(
    matrix
)


# ============================================
# CLASS NAMES
# ============================================

print()
print("========================================")
print("          ATTACK CLASSES")
print("========================================")

for index, label in enumerate(
    label_encoder.classes_
):

    print(
        f"{index}: {label}"
    )


# ============================================
# FINISHED
# ============================================

print()
print("========================================")
print("       MODEL EVALUATION COMPLETE")
print("========================================")