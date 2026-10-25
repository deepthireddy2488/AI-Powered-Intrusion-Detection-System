"""Compatibility wrappers for the shared CSV/live ML inference helper."""

from app.ml.prediction import predict_attack as predict_attack_with_confidence


def predict_attack(features: dict) -> str:
    attack_name, _confidence = predict_attack_with_confidence(features)
    return attack_name