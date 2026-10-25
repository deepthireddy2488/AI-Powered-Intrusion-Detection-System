from sqlalchemy.orm import Session

from app.models.prediction import Prediction


def create_prediction(
    db: Session,
    attack_type: str,
    severity: str,
    confidence: float,
    recommendation: str,
    user_id: int,
    session_id: str | None = None,
):
    prediction = Prediction(
        attack_type=attack_type,
        severity=severity,
        confidence=float(confidence),
        recommendation=recommendation,
        user_id=user_id,
        session_id=session_id,
    )
    try:
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        return prediction
    except Exception:
        db.rollback()
        raise


def create_predictions_bulk(db: Session, predictions_data: list, user_id: int, session_id: str):
    predictions = [
        Prediction(
            attack_type=item["attack"],
            severity=item["severity"],
            confidence=float(item["confidence"]),
            recommendation=item.get("recommendation", ""),
            row_number=item.get("row"),
            user_id=user_id,
            session_id=session_id,
        )
        for item in predictions_data
    ]
    try:
        db.add_all(predictions)
        db.commit()
        return predictions
    except Exception:
        db.rollback()
        raise


def get_predictions_by_user(db: Session, user_id: int):
    return (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.id.desc())
        .all()
    )


def get_predictions_by_session(db: Session, user_id: int, session_id: str):
    return (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id, Prediction.session_id == session_id)
        .order_by(Prediction.row_number.asc().nullslast(), Prediction.id.asc())
        .all()
    )