from fastapi import APIRouter
from app.models import HealthResponse
from app.config import config
from app.database import is_supabase_active
import os

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse)
def health_check():
    active = is_supabase_active()
    db_status = "supabase_connected" if active else "supabase_disconnected"
    return {
        "status": "healthy" if active else "degraded",
        "version": "1.0.0",
        "ocr_engine": config["ocr"].get("engine", "easyocr"),
        "database": db_status
    }
