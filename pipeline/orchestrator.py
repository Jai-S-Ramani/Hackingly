import time
import uuid
import os
from typing import Dict, Any, Optional

from pipeline.quality_analyzer import check_quality_and_tampering
from pipeline.ocr_adapter import get_ocr_adapter
from pipeline.field_extractor import extract_id_fields
from pipeline.identity_verifier import verify_identity
from pipeline.duplicate_detector import check_duplicate
from pipeline.decision_engine import evaluate_eligibility
from app.database import save_registration_and_verification, get_event_by_id

class PipelineOrchestrator:
    def __init__(self):
        self.ocr_adapter = get_ocr_adapter()

    def process_registration(
        self,
        id_image_path: str,
        selfie_path: Optional[str],
        form_name: str,
        form_email: Optional[str] = None,
        form_dob: Optional[str] = None,
        event_id: str = "hackathon-2026",
        registration_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes the autonomous 5-stage identity verification pipeline:
        Stage 1: Document Quality & Forensic Tampering (Laplacian + ELA Heatmap + EXIF)
        Stage 2: Pluggable OCR & Field Parsing (Aadhaar Verhoeff / PAN / College ID)
        Stage 3: Biometrics & Name Fuzzy Match (Face Embedding + RapidFuzz + Face Crops)
        Stage 4: Duplicate ID Prevention (SHA-256 Fingerprinting)
        Stage 5: Weighted Decision Engine (Confidence scoring & plain-English reasons)
        """
        start_time = time.time()
        reg_id = registration_id or f"reg_{uuid.uuid4().hex[:8]}"

        # 1. Fetch Event Rules from Supabase
        event_rules = {"min_age": 18, "student_only": False, "allowed_id_types": ["aadhaar", "pan", "college_id", "voter_id"]}
        try:
            ev_row = get_event_by_id(event_id)
            if ev_row:
                event_rules["min_age"] = ev_row.get("min_age") or 18
                event_rules["student_only"] = bool(ev_row.get("student_only"))
                if ev_row.get("allowed_id_types"):
                    event_rules["allowed_id_types"] = ev_row["allowed_id_types"]
        except Exception:
            pass

        # Stage 1: Quality & Tampering Forensics
        quality_res = check_quality_and_tampering(id_image_path)

        # Stage 2: OCR & Structured Extraction
        raw_blocks = self.ocr_adapter.extract_text(id_image_path)
        ocr_res = extract_id_fields(raw_blocks)

        # Stage 3: Biometric Identity Verification & Face Crop
        identity_res = verify_identity(
            id_image_path=id_image_path,
            selfie_path=selfie_path,
            form_name=form_name,
            extracted_name=ocr_res.get("name")
        )

        # Stage 4: Duplicate ID Abuse Prevention
        duplicate_res = check_duplicate(
            id_type=ocr_res.get("id_type"),
            id_number=ocr_res.get("id_number"),
            registrant_name=form_name,
            registration_id=reg_id,
            event_id=event_id
        )

        # Stage 5: Decision Engine
        decision_res = evaluate_eligibility(
            quality_res=quality_res,
            ocr_res=ocr_res,
            identity_res=identity_res,
            duplicate_res=duplicate_res,
            event_rules=event_rules
        )

        # Attach visual evidence to the breakdown
        breakdown = decision_res["breakdown"]
        breakdown["quality"]["ela_heatmap_base64"] = quality_res.get("ela_heatmap_base64")
        breakdown["identity"]["id_face_thumbnail"] = identity_res.get("face_match", {}).get("id_face_thumbnail")
        breakdown["identity"]["selfie_thumbnail"] = identity_res.get("face_match", {}).get("selfie_thumbnail")

        processing_ms = int((time.time() - start_time) * 1000)

        # Persistence
        db_payload = {
            "verification_id": f"ver_{reg_id}",
            "decision": decision_res["decision"],
            "confidence": decision_res["confidence"],
            "reason": decision_res["reason"],
            "flags": decision_res["flags"],
            "breakdown": breakdown,
            "extracted_name": ocr_res.get("name"),
            "extracted_dob": ocr_res.get("date_of_birth"),
            "extracted_id_number_masked": ocr_res.get("id_number_masked"),
            "extracted_id_type": ocr_res.get("id_type"),
            "face_match_score": identity_res.get("face_match", {}).get("score"),
            "name_match_score": identity_res.get("name_match", {}).get("score"),
            "quality_score": quality_res.get("quality_confidence"),
            "tampering_score": quality_res.get("tampering_score"),
            "is_duplicate": duplicate_res.get("is_duplicate"),
        }

        try:
            save_registration_and_verification(
                reg_id=reg_id,
                event_id=event_id,
                form_name=form_name,
                form_email=form_email,
                form_dob=form_dob,
                verification_data=db_payload
            )
        except Exception as e:
            print(f"Warning saving record: {e}")

        return {
            "registration_id": reg_id,
            "decision": decision_res["decision"],
            "confidence": decision_res["confidence"],
            "reason": decision_res["reason"],
            "flags": decision_res["flags"],
            "breakdown": breakdown,
            "processing_time_ms": processing_ms
        }

orchestrator = PipelineOrchestrator()
