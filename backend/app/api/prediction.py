from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.dependencies import get_db
from app.ml.load_model import random_forest_model
from app.ml.prediction import predict_attack
from app.ml.recommendation import get_recommendation
from app.ml.severity import get_severity
from app.repositories.analysis_session_repository import (
    complete_analysis_session,
    create_analysis_session,
)
from app.repositories.prediction_repository import (
    create_prediction,
    create_predictions_bulk,
    get_predictions_by_user,
)
from app.schemas.prediction import PredictionRequest, PredictionResponse

router = APIRouter(prefix="/predict", tags=["Prediction"])

# Protect the API from accidental or malicious oversized uploads.
MAX_CSV_SIZE_BYTES = 50 * 1024 * 1024
MAX_CSV_ROWS = 100_000


@router.get("/history")
def get_prediction_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_predictions_by_user(db=db, user_id=current_user.id)


@router.post("/", response_model=PredictionResponse)
def predict(
    request: PredictionRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    attack, confidence = predict_attack(request.features)
    severity = get_severity(attack)
    recommendation = get_recommendation(attack)

    create_prediction(
        db=db,
        attack_type=attack,
        severity=severity,
        confidence=float(confidence),
        recommendation=recommendation,
        user_id=current_user.id,
    )
    return {
        "attack_type": attack,
        "severity": severity,
        "confidence": float(confidence),
        "recommendation": recommendation,
    }


@router.post("/csv")
async def predict_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")

    # Read at most one byte over the limit so a large upload is rejected safely.
    content = await file.read(MAX_CSV_SIZE_BYTES + 1)
    if len(content) > MAX_CSV_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"CSV file exceeds the {MAX_CSV_SIZE_BYTES // (1024 * 1024)} MB limit.",
        )
    if not content:
        raise HTTPException(status_code=400, detail="The uploaded CSV file is empty.")

    filename = Path(file.filename).name
    session_id = None

    try:
        df = pd.read_csv(BytesIO(content), nrows=MAX_CSV_ROWS + 1)
        if df.empty:
            raise HTTPException(status_code=400, detail="The CSV file contains no data rows.")
        if len(df) > MAX_CSV_ROWS:
            raise HTTPException(
                status_code=413,
                detail=f"CSV contains more than {MAX_CSV_ROWS:,} rows. Split it into smaller files.",
            )

        # Drop the dataset label: it is a target field, not an input feature.
        if "Label" in df.columns:
            df = df.drop(columns=["Label"])
        df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed", case=False, na=False)]

        feature_names = list(random_forest_model.feature_names_in_)
        missing_columns = [name for name in feature_names if name not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "CSV is missing required model feature columns.",
                    "missing_columns": missing_columns,
                },
            )

        # Preserve the exact training feature order and clean invalid numeric values.
        df = df[feature_names].apply(pd.to_numeric, errors="coerce")
        df = df.replace([np.inf, -np.inf], np.nan)
        invalid_cells = int(df.isna().sum().sum())
        if invalid_cells:
            # Retain compatibility with previously tested uploads while recording
            # how much input cleaning occurred in the response.
            df = df.fillna(0)

        results = []
        for row_index, row in enumerate(df.itertuples(index=False, name=None), start=1):
            features = dict(zip(feature_names, row))
            attack, confidence = predict_attack(features)
            results.append({
                "row": row_index,
                "attack": attack,
                "severity": get_severity(attack),
                "confidence": float(confidence),
                "recommendation": get_recommendation(attack),
            })

        # Create the session only after the input has been validated and the
        # predictions have completed, avoiding empty report cards for bad files.
        analysis_session = create_analysis_session(
            db=db,
            user_id=current_user.id,
            source_type="CSV",
            name=filename,
        )
        session_id = analysis_session.session_id

        create_predictions_bulk(
            db=db,
            predictions_data=results,
            user_id=current_user.id,
            session_id=session_id,
        )
        complete_analysis_session(
            db=db,
            session_id=session_id,
            user_id=current_user.id,
        )

        safe_traffic = sum(item["attack"] == "BENIGN" for item in results)
        attacks_detected = len(results) - safe_traffic
        attack_counts = {}
        for item in results:
            if item["attack"] != "BENIGN":
                attack_counts[item["attack"]] = attack_counts.get(item["attack"], 0) + 1
        highest_attack = max(attack_counts, key=attack_counts.get) if attack_counts else "None"

        return {
            "status": "success",
            "session_id": session_id,
            "source_type": "CSV",
            "file_name": filename,
            "total_records": len(results),
            "safe_traffic": safe_traffic,
            "attacks_detected": attacks_detected,
            "highest_attack": highest_attack,
            "cleaned_invalid_cells": invalid_cells,
            "results": results,
        }

    except HTTPException:
        db.rollback()
        raise
    except Exception as error:
        db.rollback()
        if session_id:
            try:
                complete_analysis_session(
                    db=db,
                    session_id=session_id,
                    user_id=current_user.id,
                )
            except Exception:
                db.rollback()
        # Detailed stack traces remain in the server logs, not in the response.
        print(f"CSV prediction failed for user {current_user.id}: {type(error).__name__}: {error}")
        raise HTTPException(
            status_code=500,
            detail="CSV prediction failed. Check the backend logs for details.",
        ) from error