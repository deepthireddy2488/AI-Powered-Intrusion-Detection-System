from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine

# Import all models before create_all so SQLAlchemy knows every table.
from app.models.user import User  # noqa: F401
from app.models.prediction import Prediction  # noqa: F401
from app.models.attack_log import AttackLog  # noqa: F401
from app.models.analysis_session import AnalysisSession  # noqa: F401

from app.api.auth import router as auth_router
from app.api.prediction import router as prediction_router
from app.api.template import router as template_router
from app.api.attack_logs import router as attack_logs_router
from app.api.live_capture import router as live_capture_router
from app.api.analysis_sessions import router as analysis_sessions_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Powered Intrusion Detection System",
    version="1.1.0",
    description=(
        "CSV and live network intrusion analysis with session-scoped prediction "
        "history and a threat investigation timeline."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(prediction_router)
app.include_router(template_router)
app.include_router(attack_logs_router)
app.include_router(live_capture_router)
app.include_router(analysis_sessions_router)


@app.get("/")
def home():
    return {"message": "AI-Powered Intrusion Detection System API", "status": "ok"}
