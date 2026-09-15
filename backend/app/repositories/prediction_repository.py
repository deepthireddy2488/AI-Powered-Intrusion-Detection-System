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
    recommendation: str,
    user_id: int,
    session_id: str = None
):

    prediction = Prediction(
        attack_type=attack_type,
        severity=severity,
        confidence=float(confidence),
        recommendation=recommendation,
        user_id=user_id,
        session_id=session_id
    )

    db.add(prediction)

    db.commit()

    db.refresh(prediction)

    return prediction


# ==========================================
# CREATE MULTIPLE PREDICTIONS
# ==========================================

def create_predictions_bulk(
    db: Session,
    predictions_data: list,
    user_id: int,
    session_id: str
):

    predictions = []

    for item in predictions_data:

        prediction = Prediction(
            attack_type=item["attack"],
            severity=item["severity"],
            confidence=float(item["confidence"]),
            recommendation=item["recommendation"],
            user_id=user_id,
            session_id=session_id
        )

        predictions.append(prediction)

    db.add_all(predictions)

    db.commit()

    return predictions


# ==========================================
# GET USER PREDICTIONS
# ==========================================

def get_predictions_by_user(
    db: Session,
    user_id: int
):

    return (
        db.query(Prediction)
        .filter(
            Prediction.user_id == user_id
        )
        .order_by(
            Prediction.id.desc()
        )
        .all()
    )


# ==========================================
# GET PREDICTIONS FOR ONE SESSION
# ==========================================

def get_predictions_by_session(
    db: Session,
    user_id: int,
    session_id: str
):

    return (
        db.query(Prediction)
        .filter(
            Prediction.user_id == user_id,
            Prediction.session_id == session_id
        )
        .order_by(
            Prediction.id.asc()
        )
        .all()
    )