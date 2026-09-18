import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from app.models import VerificationResponse
from pipeline.orchestrator import orchestrator

router = APIRouter(tags=["Verification"])

UPLOAD_DIR = Path("data/temp_uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/verify", response_model=VerificationResponse)
async def verify_registration(
    id_image: UploadFile = File(..., description="Uploaded photo of ID card (Aadhaar/PAN/College ID)"),
    selfie: Optional[UploadFile] = File(None, description="Selfie photo of registrant"),
    form_name: str = Form(..., description="Full Name entered in registration form"),
    form_email: Optional[str] = Form(None, description="Email entered in registration form"),
    form_dob: Optional[str] = Form(None, description="Date of birth entered in form (YYYY-MM-DD)"),
    event_id: str = Form("hackathon-2026", description="Event ID to evaluate eligibility against")
):
    # Validate extension and size
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    id_ext = Path(id_image.filename or "").suffix.lower()
    if id_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported ID image format '{id_ext}'. Please upload JPEG, PNG, or WebP."
        )

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB limit
    content = await id_image.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="ID image exceeds 10MB limit. Please upload a smaller image."
        )

    # Save temp ID image
    temp_id_path = UPLOAD_DIR / f"temp_id_{os.urandom(6).hex()}{id_ext}"
    with open(temp_id_path, "wb") as buffer:
        buffer.write(content)

    temp_selfie_path = None
    if selfie and selfie.filename:
        selfie_ext = Path(selfie.filename).suffix.lower()
        if selfie_ext in allowed_extensions:
            temp_selfie_path = UPLOAD_DIR / f"temp_selfie_{os.urandom(6).hex()}{selfie_ext}"
            with open(temp_selfie_path, "wb") as buffer:
                shutil.copyfileobj(selfie.file, buffer)

    try:
        result = orchestrator.process_registration(
            id_image_path=str(temp_id_path),
            selfie_path=str(temp_selfie_path) if temp_selfie_path else None,
            form_name=form_name,
            form_email=form_email,
            form_dob=form_dob,
            event_id=event_id
        )
        return result
    finally:
        # Clean up temporary uploads to respect participant privacy
        if temp_id_path.exists():
            try:
                os.remove(temp_id_path)
            except Exception:
                pass
        if temp_selfie_path and temp_selfie_path.exists():
            try:
                os.remove(temp_selfie_path)
            except Exception:
                pass
