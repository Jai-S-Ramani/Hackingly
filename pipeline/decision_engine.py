from datetime import datetime
from typing import Dict, Any, List, Optional
from app.config import config

class DecisionEngine:
    def __init__(self):
        dec_cfg = config["decision"]
        self.weights = dec_cfg.get("weights", {
            "quality": 0.10,
            "ocr": 0.20,
            "face": 0.30,
            "name": 0.25,
            "duplicate": 0.15,
        })
        self.approve_threshold = dec_cfg.get("approve_threshold", 0.75)
        self.review_threshold = dec_cfg.get("review_threshold", 0.50)

    def decide(
        self,
        quality_res: Dict[str, Any],
        ocr_res: Dict[str, Any],
        identity_res: Dict[str, Any],
        duplicate_res: Dict[str, Any],
        event_rules: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Runs Stage 5 Decision Engine:
        1. Computes weighted confidence score from all stages.
        2. Applies event eligibility criteria (age, student verification).
        3. Assigns 3-tier status: 'approved', 'manual_review', 'rejected'.
        4. Produces human-readable reason string.
        """
        event_rules = event_rules or {"min_age": 18, "student_only": False}
        all_flags: List[str] = []
        all_flags.extend(quality_res.get("flags", []))
        all_flags.extend(identity_res.get("flags", []))
        all_flags.extend(duplicate_res.get("flags", []))

        # Individual Stage Scores (0.0 to 1.0)
        s_quality = quality_res.get("quality_confidence", 0.8)
        s_ocr = ocr_res.get("extraction_confidence", 0.7)

        # Face score: If selfie wasn't provided, don't penalize harshly, use neutral 0.65
        face_info = identity_res.get("face_match", {})
        if face_info.get("score") is not None:
            s_face = face_info["score"]
        else:
            s_face = 0.65 # Neutral when selfie omitted

        # Name match score (normalized from 0-100 to 0-1)
        name_info = identity_res.get("name_match", {})
        s_name = (name_info.get("score", 50.0)) / 100.0

        # Duplicate score (1.0 if clean, 0.0 if reused under different name)
        s_dup = 0.0 if duplicate_res.get("is_duplicate", False) else 1.0

        # Weighted calculation
        final_confidence = (
            self.weights["quality"] * s_quality +
            self.weights["ocr"] * s_ocr +
            self.weights["face"] * s_face +
            self.weights["name"] * s_name +
            self.weights["duplicate"] * s_dup
        )
        final_confidence = max(0.0, min(1.0, round(final_confidence, 2)))

        # Age Check (DEFECT-006)
        age_passed = True
        computed_age = None
        dob_str = ocr_res.get("date_of_birth")
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d")
                today = datetime.now()
                computed_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                min_age = event_rules.get("min_age", 18)
                if computed_age < min_age:
                    age_passed = False
                    all_flags.append(f"underage_participant_{computed_age}_years")
            except Exception:
                all_flags.append("age_unverified")
        else:
            # Missing or unreadable date of birth must not silently pass
            all_flags.append("age_unverified")

        # Aadhaar / ID Checksum Validation (DEFECT-003)
        if ocr_res.get("checksum_valid") is False:
            all_flags.append("invalid_id_checksum")

        # Student Only Check
        student_passed = True
        if event_rules.get("student_only", False):
            if ocr_res.get("id_type") != "college_id":
                student_passed = False
                all_flags.append("event_requires_college_id")

        # --- Decision Logic ---
        decision = "manual_review"
        reasons = []

        # Hard Rejection Conditions
        if duplicate_res.get("is_duplicate"):
            decision = "rejected"
            if "user_already_registered" in all_flags:
                reasons.append("User Already Entered: A registration with this identification document has already been submitted for this event.")
            else:
                reasons.append("Duplicate ID detected: This document was already registered by another participant.")
        elif "invalid_id_checksum" in all_flags:
            decision = "rejected"
            reasons.append("Invalid ID Checksum: Document failed Verhoeff mathematical integrity check (probable fake ID).")
        elif not age_passed:
            decision = "rejected"
            reasons.append(f"Age restriction failure: Participant is {computed_age} years old (minimum {event_rules.get('min_age', 18)}+ required).")
        elif "potential_tampering_ela" in all_flags or any("editing_software" in f for f in all_flags):
            decision = "rejected"
            reasons.append("Document tampering detected: Image exhibits digital modification or editing artifacts.")
        elif not student_passed:
            decision = "rejected"
            reasons.append("Eligibility requirement failed: Event requires a valid College / Student ID.")
        elif quality_res.get("blur_score", 150) < 50.0:
            decision = "rejected"
            reasons.append("Unreadable document: Image is too blurry for reliable identification. Please re-upload.")

        # Approval Conditions
        elif final_confidence >= self.approve_threshold and not all_flags:
            decision = "approved"
            reasons.append("All checks passed successfully. Identity and eligibility verified with high confidence.")
        elif final_confidence >= self.approve_threshold and all(f in ["selfie_missing"] for f in all_flags):
            decision = "approved"
            reasons.append("Identity verified. Document matches submitted details.")

        # Manual Review for Borderline / Low False Positives
        else:
            decision = "manual_review"
            flag_desc = []
            if "blurry_image" in all_flags:
                flag_desc.append("low image clarity")
            if "name_partial_match" in all_flags or "name_mismatch" in all_flags:
                flag_desc.append("minor name discrepancy")
            if "face_match_uncertain" in all_flags:
                flag_desc.append("face match uncertain")
            if "selfie_missing" in all_flags:
                flag_desc.append("no selfie provided")
            
            reasons.append(f"Borderline confidence ({int(final_confidence*100)}%): Routed for manual review due to {', '.join(flag_desc) if flag_desc else 'verification review'}.")

        primary_reason = " ".join(reasons)

        return {
            "decision": decision,
            "confidence": final_confidence,
            "reason": primary_reason,
            "flags": all_flags,
            "breakdown": {
                "quality": {
                    "score": s_quality,
                    "blur_score": quality_res.get("blur_score"),
                    "tampering_score": quality_res.get("tampering_score"),
                    "resolution_ok": quality_res.get("resolution_ok"),
                    "detected_doc_type": ocr_res.get("id_type"),
                },
                "extraction": {
                    "score": s_ocr,
                    "name": ocr_res.get("name"),
                    "date_of_birth": ocr_res.get("date_of_birth"),
                    "id_number_masked": ocr_res.get("id_number_masked"),
                    "id_type": ocr_res.get("id_type"),
                    "format_valid": ocr_res.get("format_valid", True),
                    "checksum_valid": ocr_res.get("checksum_valid"),
                },
                "identity": {
                    "face_match_score": face_info.get("score"),
                    "face_match_verdict": face_info.get("verdict"),
                    "name_match_score": name_info.get("score"),
                    "name_match_verdict": name_info.get("verdict"),
                },
                "duplicate": {
                    "is_duplicate": duplicate_res.get("is_duplicate"),
                    "details": duplicate_res.get("details"),
                },
                "eligibility": {
                    "age_check": "pass" if (age_passed and dob_str) else ("unverified" if not dob_str else "fail"),
                    "computed_age": computed_age,
                    "student_check": "pass" if student_passed else "fail",
                }
            }
        }

def evaluate_eligibility(
    quality_res: Dict[str, Any],
    ocr_res: Dict[str, Any],
    identity_res: Dict[str, Any],
    duplicate_res: Dict[str, Any],
    event_rules: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    engine = DecisionEngine()
    return engine.decide(quality_res, ocr_res, identity_res, duplicate_res, event_rules)
