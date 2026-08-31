import joblib
import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]


# ============================================================
# MODEL PATHS
# ============================================================

MODEL_PATH = BASE_DIR / "ml" / "models" / "random_forest.pkl"
FEATURES_PATH = BASE_DIR / "ml" / "models" / "features.pkl"
ENCODER_PATH = BASE_DIR / "ml" / "models" / "label_encoder.pkl"


# ============================================================
# CHECK FILES
# ============================================================

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}"
    )

if not FEATURES_PATH.exists():
    raise FileNotFoundError(
        f"Feature file not found: {FEATURES_PATH}"
    )

if not ENCODER_PATH.exists():
    raise FileNotFoundError(
        f"Label encoder file not found: {ENCODER_PATH}"
    )


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

model = joblib.load(MODEL_PATH)


# ============================================================
# LOAD FEATURE NAMES
# ============================================================

feature_names = joblib.load(FEATURES_PATH)


# Convert to normal Python list
feature_names = list(feature_names)


# ============================================================
# LOAD LABEL ENCODER
# ============================================================

label_encoder = joblib.load(ENCODER_PATH)


# ============================================================
# VERIFY FEATURE COUNT
# ============================================================

EXPECTED_FEATURE_COUNT = 78

if len(feature_names) != EXPECTED_FEATURE_COUNT:
    raise ValueError(
        f"Feature count mismatch. "
        f"Expected {EXPECTED_FEATURE_COUNT}, "
        f"but loaded {len(feature_names)}."
    )


print("===================================")
print(" AI IDS MODEL LOADED")
print("===================================")
print(f"Model: {type(model).__name__}")
print(f"Features: {len(feature_names)}")
print("Label Encoder: Loaded")
print("===================================")


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_attack(features):

    # --------------------------------------------------------
    # CHECK FEATURE COUNT
    # --------------------------------------------------------

    if len(features) != EXPECTED_FEATURE_COUNT:

        raise ValueError(
            f"Invalid feature count. "
            f"Expected {EXPECTED_FEATURE_COUNT}, "
            f"received {len(features)}."
        )


    # --------------------------------------------------------
    # CREATE DATAFRAME
    # --------------------------------------------------------
    # IMPORTANT:
    # The columns are placed in EXACTLY the same order
    # used during model training.
    # --------------------------------------------------------

    df = pd.DataFrame(
        [features],
        columns=feature_names
    )


    # --------------------------------------------------------
    # CONVERT VALUES TO NUMERIC
    # --------------------------------------------------------

    df = df.apply(
        pd.to_numeric,
        errors="coerce"
    )


    # --------------------------------------------------------
    # CHECK FOR INVALID VALUES
    # --------------------------------------------------------

    if df.isnull().any().any():

        invalid_columns = df.columns[
            df.isnull().any()
        ].tolist()

        raise ValueError(
            "Invalid or missing feature values in: "
            f"{invalid_columns}"
        )


    # --------------------------------------------------------
    # AI PREDICTION
    # --------------------------------------------------------

    prediction = model.predict(df)[0]


    # --------------------------------------------------------
    # CONVERT ENCODED LABEL TO ATTACK NAME
    # --------------------------------------------------------

    attack_name = label_encoder.inverse_transform(
        [prediction]
    )[0]


    return attack_name