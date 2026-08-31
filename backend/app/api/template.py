from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path
import joblib
import pandas as pd

router = APIRouter(
    prefix="/predict",
    tags=["Template"]
)

BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_DIR = BASE_DIR / "ml" / "models"

features = joblib.load(MODEL_DIR / "features.pkl")


@router.get("/template")
def download_template():

    df = pd.DataFrame(columns=features)

    template_path = BASE_DIR / "ml" / "models" / "prediction_template.csv"

    df.to_csv(template_path, index=False)

    return FileResponse(
        path=template_path,
        filename="prediction_template.csv",
        media_type="text/csv"
    )