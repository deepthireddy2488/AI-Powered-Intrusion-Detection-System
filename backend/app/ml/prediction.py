from app.ml.load_model import random_forest_model, label_encoder


def predict_attack(features: dict):

    feature_names = list(random_forest_model.feature_names_in_)

    missing_features = [
        name for name in feature_names
        if name not in features
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    input_data = [
        [features[name] for name in feature_names]
    ]

    prediction = random_forest_model.predict(input_data)

    probabilities = random_forest_model.predict_proba(input_data)

    confidence = round(
        max(probabilities[0]) * 100,
        2
    )

    attack = label_encoder.inverse_transform(
        prediction
    )[0]

    return attack, confidence