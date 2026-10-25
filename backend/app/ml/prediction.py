"""Shared, feature-name-safe inference used by CSV and live traffic."""

import numpy as np
import pandas as pd

from app.ml.load_model import random_forest_model, label_encoder

FEATURE_NAMES = list(random_forest_model.feature_names_in_)
EXPECTED_FEATURE_COUNT = len(FEATURE_NAMES)

if EXPECTED_FEATURE_COUNT != 78:
    raise ValueError(
        f"Expected 78 trained features, but the loaded model exposes {EXPECTED_FEATURE_COUNT}."
    )


def predict_attack(features: dict) -> tuple[str, float]:
    """Return (decoded attack label, confidence percentage from 0 to 100)."""
    if not isinstance(features, dict):
        raise TypeError("Prediction features must be provided as a dictionary.")

    missing = [name for name in FEATURE_NAMES if name not in features]
    if missing:
        raise ValueError(f"Missing required features: {missing}")

    ordered = {name: features[name] for name in FEATURE_NAMES}
    frame = pd.DataFrame([ordered], columns=FEATURE_NAMES)
    frame = frame.apply(pd.to_numeric, errors="coerce")
    frame = frame.replace([np.inf, -np.inf], np.nan)

    if frame.isna().any().any():
        invalid_columns = frame.columns[frame.isna().any()].tolist()
        raise ValueError(f"Missing or invalid numeric values in features: {invalid_columns}")

    encoded_prediction = random_forest_model.predict(frame)[0]
    attack_name = str(label_encoder.inverse_transform([encoded_prediction])[0])

    if hasattr(random_forest_model, "predict_proba"):
        probabilities = random_forest_model.predict_proba(frame)[0]
        confidence = round(float(np.max(probabilities)) * 100.0, 2)
    else:
        confidence = 0.0

    return attack_name, confidence