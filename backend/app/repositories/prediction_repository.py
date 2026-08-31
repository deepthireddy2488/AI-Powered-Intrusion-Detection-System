from sqlalchemy.orm import Session

from app.models.prediction import Prediction


# ==========================================
# CREATE SINGLE PREDICTION
# ==========================================

def create_prediction(
    db: Session,
    attack_type: str,
    severity: str,
    confidence: float,
    recommendation: str
):

    prediction = Prediction(
        attack_type=attack_type,
        severity=severity,
        confidence=confidence,
        recommendation=recommendation
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction


# ==========================================
# CREATE MULTIPLE PREDICTIONS AT ONCE
# ==========================================

def create_predictions_bulk(
    db: Session,
    predictions_data: list
):

    predictions = []

    for item in predictions_data:

        prediction = Prediction(
            attack_type=item["attack"],
            severity=item["severity"],
            confidence=float(item["confidence"]),
            recommendation=item["recommendation"]
        )

        predictions.append(prediction)


    # Add all predictions together
    db.add_all(predictions)

    # Commit only once
    db.commit()

    return predictions


# ==========================================
# GET ALL PREDICTIONS
# ==========================================

def get_all_predictions(db: Session):

    return (
        db.query(Prediction)
        .order_by(Prediction.id.desc())
        .all()
    )