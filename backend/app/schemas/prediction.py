from pydantic import BaseModel


class PredictionRequest(BaseModel):
    features: dict


class PredictionResponse(BaseModel):
    attack_type: str
    severity: str
    confidence: float
    recommendation: str
    