from fastapi import APIRouter, UploadFile, File, Depends
import pandas as pd
import joblib
from pathlib import Path
from collections import Counter
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.prediction_repository import create_prediction
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/predict",
    tags=["CSV Prediction"]
)


# ==========================================
# PROJECT ROOT
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[3]


# ==========================================
# ML MODELS FOLDER
# ==========================================

MODEL_DIR = BASE_DIR / "ml" / "models"


# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load(
    MODEL_DIR / "random_forest.pkl"
)

label_encoder = joblib.load(
    MODEL_DIR / "label_encoder.pkl"
)

features = joblib.load(
    MODEL_DIR / "features.pkl"
)


# ==========================================
# CSV PREDICTION
# ==========================================

@router.post("/csv")
async def predict_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # ==========================================
    # READ CSV
    # ==========================================

    df = pd.read_csv(file.file)


    # ==========================================
    # CHECK REQUIRED COLUMNS
    # ==========================================

    missing_columns = [
        col
        for col in features
        if col not in df.columns
    ]


    if missing_columns:

        return {
            "status": "error",
            "missing_columns": missing_columns
        }


    # ==========================================
    # ARRANGE FEATURES
    # ==========================================

    X = df[features]


    # ==========================================
    # PREDICT
    # ==========================================

    predictions = model.predict(X)


    # ==========================================
    # CONVERT LABELS TO ATTACK NAMES
    # ==========================================

    attack_names = label_encoder.inverse_transform(
        predictions
    )


    # Add prediction column
    df["Prediction"] = attack_names


    # ==========================================
    # COUNT PREDICTIONS
    # ==========================================

    counter = Counter(attack_names)


    # Safe traffic count
    safe_count = counter.get(
        "BENIGN",
        0
    )


    # Attack count
    attack_count = len(df) - safe_count


    # ==========================================
    # HIGHEST OCCURRING ATTACK
    # ==========================================

    attack_counter = {
        attack: count
        for attack, count in counter.items()
        if attack != "BENIGN"
    }


    highest_attack = (
        max(
            attack_counter,
            key=attack_counter.get
        )
        if attack_counter
        else "None"
    )


    # ==========================================
    # CREATE DETAILED RESULTS
    # ==========================================

    results = []


    for index, attack in enumerate(
        attack_names,
        start=1
    ):

        if attack == "BENIGN":

            severity = "Low"

            recommendation = (
                "Normal Traffic"
            )

        elif attack in [
            "DDoS",
            "DoS Hulk",
            "DoS GoldenEye"
        ]:

            severity = "High"

            recommendation = (
                "Block Source IP Immediately"
            )

        elif attack in [
            "PortScan",
            "Bot"
        ]:

            severity = "Medium"

            recommendation = (
                "Investigate Network Activity"
            )

        else:

            severity = "Medium"

            recommendation = (
                "Review Security Logs"
            )


        results.append({
            "row": index,
            "attack": attack,
            "severity": severity,
            "recommendation": recommendation
        })


        # ==========================================
        # SAVE WITH CURRENT USER
        # ==========================================

        create_prediction(
            db=db,
            attack_type=attack,
            severity=severity,
            confidence=100.0,
            recommendation=recommendation,
            user_id=current_user.id
        )


    # ==========================================
    # RETURN RESPONSE
    # ==========================================

    return {
        "status": "success",
        "total_records": len(df),
        "safe_traffic": safe_count,
        "attacks_detected": attack_count,
        "highest_attack": highest_attack,
        "results": results
    }