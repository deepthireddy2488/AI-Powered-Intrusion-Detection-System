from fastapi import APIRouter, UploadFile, File
import pandas as pd
import joblib
from pathlib import Path
from collections import Counter
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database.dependencies import get_db
from app.repositories.prediction_repository import create_prediction

router = APIRouter(
    prefix="/predict",
    tags=["CSV Prediction"]
)

# Project Root
BASE_DIR = Path(__file__).resolve().parents[3]

# ML Models Folder
MODEL_DIR = BASE_DIR / "ml" / "models"

# Load Model
model = joblib.load(MODEL_DIR / "random_forest.pkl")
label_encoder = joblib.load(MODEL_DIR / "label_encoder.pkl")
features = joblib.load(MODEL_DIR / "features.pkl")


@router.post("/csv")
async def predict_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Read uploaded CSV
    df = pd.read_csv(file.file)

    # Check required columns
    missing_columns = [
        col for col in features
        if col not in df.columns
    ]

    if missing_columns:
        return {
            "status": "error",
            "missing_columns": missing_columns
        }

    # Arrange columns in the same order used during training
    X = df[features]

    # Predict
    predictions = model.predict(X)

    # Convert numeric labels to attack names
    attack_names = label_encoder.inverse_transform(predictions)

    # Add prediction column
    df["Prediction"] = attack_names

    # Count each prediction
    counter = Counter(attack_names)

    # Safe traffic count
    safe_count = counter.get("BENIGN", 0)

    # Attack count
    attack_count = len(df) - safe_count

    # Highest occurring attack (excluding BENIGN)
    attack_counter = {
        attack: count
        for attack, count in counter.items()
        if attack != "BENIGN"
    }

    highest_attack = (
        max(attack_counter, key=attack_counter.get)
        if attack_counter
        else "None"
    )

    # Create detailed prediction list
    results = []

    for index, attack in enumerate(attack_names, start=1):

        if attack == "BENIGN":
            severity = "Low"
            recommendation = "Normal Traffic"

        elif attack in ["DDoS", "DoS Hulk", "DoS GoldenEye"]:
            severity = "High"
            recommendation = "Block Source IP Immediately"

        elif attack in ["PortScan", "Bot"]:
            severity = "Medium"
            recommendation = "Investigate Network Activity"

        else:
            severity = "Medium"
            recommendation = "Review Security Logs"

        results.append({
            "row": index,
            "attack": attack,
            "severity": severity,
            "recommendation": recommendation
        })
        create_prediction(
            db=db,
            attack_type=attack,
            severity=severity,
            confidence=100.0,
            recommendation=recommendation
        )

    return {
        "status": "success",
        "total_records": len(df),
        "safe_traffic": safe_count,
        "attacks_detected": attack_count,
        "highest_attack": highest_attack,
        "results": results
    }