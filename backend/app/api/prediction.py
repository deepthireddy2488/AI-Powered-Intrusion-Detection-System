from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

import pandas as pd
import numpy as np

from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.ml.prediction import predict_attack
from app.ml.severity import get_severity
from app.ml.recommendation import get_recommendation
from app.ml.load_model import random_forest_model

from app.database.dependencies import get_db
from app.repositories.prediction_repository import (
    create_prediction,
    create_predictions_bulk
)


router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


# ==========================================
# SINGLE PREDICTION
# ==========================================

@router.post("/", response_model=PredictionResponse)
def predict(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):

    attack, confidence = predict_attack(request.features)

    severity = get_severity(attack)

    recommendation = get_recommendation(attack)

    create_prediction(
        db=db,
        attack_type=attack,
        severity=severity,
        confidence=float(confidence),
        recommendation=recommendation
    )

    return {
        "attack_type": attack,
        "severity": severity,
        "confidence": float(confidence),
        "recommendation": recommendation
    }


# ==========================================
# CSV FILE PREDICTION
# ==========================================

@router.post("/csv")
async def predict_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename or not file.filename.lower().endswith(".csv"):

        return {
            "status": "error",
            "message": "Please upload a CSV file."
        }

    try:

        print("Reading CSV file...")

        # Read uploaded CSV
        df = pd.read_csv(file.file)

        print("Total CSV rows:", len(df))
        print("Total CSV columns:", len(df.columns))


        # ==========================================
        # REMOVE LABEL COLUMN
        # ==========================================

        if "Label" in df.columns:

            df = df.drop(columns=["Label"])


        # Remove unnamed columns if present
        df = df.loc[
            :,
            ~df.columns.str.contains(
                "^Unnamed",
                case=False,
                na=False
            )
        ]


        # ==========================================
        # GET EXACT MODEL FEATURE NAMES
        # ==========================================

        feature_names = list(
            random_forest_model.feature_names_in_
        )

        print("Model requires features:", len(feature_names))


        # Check missing columns
        missing_columns = [
            column
            for column in feature_names
            if column not in df.columns
        ]


        if missing_columns:

            print("Missing columns:", missing_columns)

            return {
                "status": "error",
                "message": "CSV is missing required columns.",
                "missing_columns": missing_columns
            }


        # Keep features in exact training order
        df = df[feature_names]


        # ==========================================
        # CLEAN DATA
        # ==========================================

        df = df.replace(
            [np.inf, -np.inf],
            0
        )

        df = df.fillna(0)


        # ==========================================
        # START PREDICTION
        # ==========================================

        print("Starting predictions...")

        results = []


        for index, row in df.iterrows():

            # IMPORTANT:
            # predict_attack expects a dictionary
            features = row.to_dict()


            # AI model prediction
            attack, confidence = predict_attack(
                features
            )


            # Severity
            severity = get_severity(attack)


            # Recommendation
            recommendation = get_recommendation(
                attack
            )


            # Add prediction result
            results.append({
                "row": int(index) + 1,
                "attack": attack,
                "severity": severity,
                "confidence": float(confidence),
                "recommendation": recommendation
            })


        print("Predictions completed.")


        # ==========================================
        # SAVE ALL RESULTS AT ONCE
        # ==========================================

        print("Saving predictions to database...")

        create_predictions_bulk(
            db=db,
            predictions_data=results
        )

        print("Database saving completed.")


        # ==========================================
        # CALCULATE SUMMARY
        # ==========================================

        safe_traffic = sum(
            1
            for item in results
            if item["attack"] == "BENIGN"
        )


        attacks_detected = sum(
            1
            for item in results
            if item["attack"] != "BENIGN"
        )


        # Count attack types
        attack_counts = {}


        for item in results:

            attack = item["attack"]

            if attack != "BENIGN":

                attack_counts[attack] = (
                    attack_counts.get(attack, 0) + 1
                )


        highest_attack = "None"


        if attack_counts:

            highest_attack = max(
                attack_counts,
                key=attack_counts.get
            )


        print("Sending response to frontend...")


        # ==========================================
        # RETURN RESULT
        # ==========================================

        return {
            "status": "success",
            "total_records": len(results),
            "safe_traffic": safe_traffic,
            "attacks_detected": attacks_detected,
            "highest_attack": highest_attack,
            "results": results
        }


    except Exception as e:

        print("CSV Prediction Error:")
        print(str(e))

        return {
            "status": "error",
            "message": str(e)
        }