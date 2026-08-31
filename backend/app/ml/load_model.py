import joblib
from pathlib import Path

# Get the backend folder
BASE_DIR = Path(__file__).resolve().parents[2]

# Path to the ML models folder
MODEL_DIR = BASE_DIR.parent / "ml" / "models"

# Load trained model
random_forest_model = joblib.load(
    MODEL_DIR / "random_forest.pkl"
)

# Load label encoder
label_encoder = joblib.load(
    MODEL_DIR / "label_encoder.pkl"
)