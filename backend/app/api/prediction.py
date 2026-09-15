from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

import pandas as pd
import numpy as np

from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.ml.prediction import predict_attack
from app.ml.severity import get_severity
from app.ml.recommendation import get_recommendation
from app.ml.load_model import random_forest_model

from app.repositories.prediction_repository import (
    create_prediction,
    create_predictions_bulk,
    get_predictions_by_user
)

from app.repositories.analysis_session_repository import (
    create_analysis_session,
    complete_analysis_session
)

from app.database.dependencies import get_db
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


# ==========================================
# CURRENT USER PREDICTION HISTORY
# ==========================================

@router.get("/history")
def get_prediction_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_predictions_by_user(
        db=db,
        user_id=current_user.id
    )


# ==========================================
# SINGLE PREDICTION
# ==========================================

@router.post("/", response_model=PredictionResponse)
def predict(
    request: PredictionRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    attack, confidence = predict_attack(
        request.features
    )

    severity = get_severity(attack)

    recommendation = get_recommendation(attack)

    create_prediction(
        db=db,
        attack_type=attack,
        severity=severity,
        confidence=float(confidence),
        recommendation=recommendation,
        user_id=current_user.id
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
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # ==========================================
    # CHECK FILE
    # ==========================================

    if not file.filename or not file.filename.lower().endswith(".csv"):

        return {
            "status": "error",
            "message": "Please upload a CSV file."
        }

    try:

        print("===================================")
        print("CSV PREDICTION STARTED")
        print("User ID:", current_user.id)
        print("File:", file.filename)
        print("===================================")


        # ==========================================
        # READ CSV
        # ==========================================

        print("Reading CSV file...")

        df = pd.read_csv(file.file)

        print("Total CSV rows:", len(df))
        print("Total CSV columns:", len(df.columns))


        # ==========================================
        # REMOVE LABEL COLUMN
        # ==========================================

        if "Label" in df.columns:

            df = df.drop(
                columns=["Label"]
            )


        # ==========================================
        # REMOVE UNNAMED COLUMNS
        # ==========================================

        df = df.loc[
            :,
            ~df.columns.str.contains(
                "^Unnamed",
                case=False,
                na=False
            )
        ]


        # ==========================================
        # GET MODEL FEATURES
        # ==========================================

        feature_names = list(
            random_forest_model.feature_names_in_
        )

        print(
            "Model requires features:",
            len(feature_names)
        )


        # ==========================================
        # CHECK MISSING COLUMNS
        # ==========================================

        missing_columns = [
            column
            for column in feature_names
            if column not in df.columns
        ]

        if missing_columns:

            print(
                "Missing columns:",
                missing_columns
            )

            return {
                "status": "error",
                "message": "CSV is missing required columns.",
                "missing_columns": missing_columns
            }


        # ==========================================
        # KEEP EXACT MODEL FEATURE ORDER
        # ==========================================

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
        # CREATE NEW ANALYSIS SESSION
        # ==========================================

        analysis_session = create_analysis_session(
            db=db,
            user_id=current_user.id,
            source_type="CSV",
            name=file.filename
        )

        session_id = analysis_session.session_id

        print("===================================")
        print("NEW CSV SESSION CREATED")
        print("Session ID:", session_id)
        print("===================================")


        # ==========================================
        # START PREDICTION
        # ==========================================

        print("Starting predictions...")

        results = []


        for index, row in df.iterrows():

            # Convert row to dictionary
            features = row.to_dict()


            # AI model prediction
            attack, confidence = predict_attack(
                features
            )


            # Severity
            severity = get_severity(
                attack
            )


            # Recommendation
            recommendation = get_recommendation(
                attack
            )


            # Save result
            results.append({
                "row": int(index) + 1,
                "attack": attack,
                "severity": severity,
                "confidence": float(confidence),
                "recommendation": recommendation
            })


        print("Predictions completed.")


        # ==========================================
        # SAVE RESULTS WITH SESSION ID
        # ==========================================

        print("Saving predictions to database...")

        create_predictions_bulk(
            db=db,
            predictions_data=results,
            user_id=current_user.id,
            session_id=session_id
        )

        print("Database saving completed.")


        # ==========================================
        # MARK SESSION AS COMPLETED
        # ==========================================

        complete_analysis_session(
            db=db,
            session_id=session_id
        )


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


        # ==========================================
        # COUNT ATTACK TYPES
        # ==========================================

        attack_counts = {}


        for item in results:

            attack = item["attack"]

            if attack != "BENIGN":

                attack_counts[attack] = (
                    attack_counts.get(
                        attack,
                        0
                    ) + 1
                )


        highest_attack = "None"


        if attack_counts:

            highest_attack = max(
                attack_counts,
                key=attack_counts.get
            )


        # ==========================================
        # RETURN RESULT
        # ==========================================

        print("===================================")
        print("CSV PREDICTION COMPLETED")
        print("Session ID:", session_id)
        print("Total:", len(results))
        print("Safe:", safe_traffic)
        print("Attacks:", attacks_detected)
        print("===================================")


        return {
            "status": "success",

            "session_id": session_id,

            "source_type": "CSV",

            "file_name": file.filename,

            "total_records": len(results),

            "safe_traffic": safe_traffic,

            "attacks_detected": attacks_detected,

            "highest_attack": highest_attack,

            "results": results
        }


    except Exception as e:

        print("===================================")
        print("CSV PREDICTION ERROR")
        print(str(e))
        print("===================================")

        return {
            "status": "error",
            "message": str(e)
        }