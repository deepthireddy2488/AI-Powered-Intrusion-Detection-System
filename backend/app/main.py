from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.live_capture import router as live_capture_router

from app.api.attack_logs import router as attack_logs_router

from app.database.database import Base, engine

# Import all models
from app.models.user import User
from app.models.prediction import Prediction
from app.models.attack_log import AttackLog

from app.api.auth import router as auth_router
from app.api.prediction import router as prediction_router
from app.api.csv_prediction import router as csv_prediction_router
from app.api.template import router as template_router


# ============================================
# CREATE DATABASE TABLES
# ============================================

Base.metadata.create_all(bind=engine)


# ============================================
# FASTAPI APPLICATION
# ============================================

app = FastAPI(
    title="AI-Powered Intrusion Detection System",
    version="1.0.0"
)


# ============================================
# CORS
# ============================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ============================================
# ROUTES
# ============================================

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    prediction_router
)

app.include_router(
    csv_prediction_router
)

app.include_router(
    template_router
)

# Attack Logs
app.include_router(
    attack_logs_router
)
# Live Capture
app.include_router(
    live_capture_router
)


# ============================================
# HOME
# ============================================

@app.get("/")
def home():

    return {
        "message":
            "AI-Powered Intrusion Detection System API"
    }