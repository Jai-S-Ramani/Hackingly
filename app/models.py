from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class QualityBreakdown(BaseModel):
    score: float
    blur_score: float
    tampering_score: float
    resolution_ok: bool
    detected_doc_type: str

class ExtractionBreakdown(BaseModel):
    score: float
    name: Optional[str] = None
    date_of_birth: Optional[str] = None
    id_number_masked: Optional[str] = None
    id_type: Optional[str] = None
    format_valid: bool = True
    checksum_valid: Optional[bool] = None

class IdentityBreakdown(BaseModel):
    face_match_score: Optional[float] = None
    face_match_verdict: Optional[str] = None
    name_match_score: float
    name_match_verdict: str

class DuplicateBreakdown(BaseModel):
    is_duplicate: bool
    details: Optional[str] = None

class EligibilityBreakdown(BaseModel):
    age_check: str
    computed_age: Optional[int] = None
    student_check: str

class VerificationBreakdown(BaseModel):
    quality: Optional[Dict[str, Any]] = None
    extraction: Optional[Dict[str, Any]] = None
    identity: Optional[Dict[str, Any]] = None
    duplicate: Optional[Dict[str, Any]] = None
    eligibility: Optional[Dict[str, Any]] = None

class VerificationResponse(BaseModel):
    registration_id: str
    decision: str = Field(..., description="approved | manual_review | rejected")
    confidence: float
    reason: str
    flags: List[str] = []
    breakdown: Optional[Dict[str, Any]] = None
    processing_time_ms: int

class EventCreateRequest(BaseModel):
    id: str
    name: str
    min_age: int = 18
    max_age: Optional[int] = None
    student_only: bool = False
    allowed_id_types: List[str] = ["aadhaar", "pan", "college_id", "voter_id"]

class HealthResponse(BaseModel):
    status: str
    version: str
    ocr_engine: str
    database: str
