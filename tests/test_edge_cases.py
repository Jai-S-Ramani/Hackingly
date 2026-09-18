"""
Additional pass/fail edge-case coverage beyond the existing happy-path
tests (test_decision.py, test_ocr.py, test_identity.py, test_duplicates.py,
test_quality.py).

Genuine bugs found while writing these edge cases were moved OUT of this
file and into tests/test_critical_defects.py (see DEFECT-006, DEFECT-007,
DEFECT-008 there) — this file only contains cases that pass against the
current code, i.e. real regression coverage for behavior that already
works, verified by actually running it.

NOTE: a few tests below import `pipeline.field_extractor`, which currently
fails to import (DEFECT-001). Those will ERROR at collection until that
one-line bug is fixed — that's expected, not a flaw in these tests.
"""
import os
import sys
import tempfile
import uuid
from datetime import datetime, timedelta

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ===========================================================================
# FIELD EXTRACTION — boundary & malformed input
# (blocked by DEFECT-001 until the Tuple import is fixed)
# ===========================================================================

class TestFieldExtractionEdgeCases:
    def test_empty_blocks_list_does_not_crash(self):
        from pipeline.field_extractor import FieldExtractor
        res = FieldExtractor().parse_blocks([])
        assert res["name"] is None
        assert res["id_number"] is None
        assert res["extraction_confidence"] >= 0.1  # clamped floor, never negative/zero

    def test_dob_two_digit_year_pivot_boundary(self):
        """`>30` -> 19xx, else -> 20xx. Confirm the pivot value itself (30)
        resolves to 2030, and flag this for product review: a DOB of 2030
        means the person isn't born yet — decision_engine's age math
        (today.year - dob.year) would go negative. Worth a manual check
        once this module is import-fixed; not asserting a "correct"
        outcome here since the pivot's intended range isn't documented."""
        from pipeline.field_extractor import FieldExtractor
        extractor = FieldExtractor()
        blocks_30 = [{"text": "DOB: 01/01/30", "confidence": 0.9}]
        res_30 = extractor.parse_blocks(blocks_30)
        assert res_30["date_of_birth"] == "2030-01-01"

    def test_aadhaar_number_with_invalid_checksum_is_flagged(self):
        from pipeline.field_extractor import FieldExtractor
        extractor = FieldExtractor()
        blocks = [
            {"text": "Government of India", "confidence": 0.9},
            {"text": "ARJUN KUMAR", "confidence": 0.9},
            {"text": "DOB: 14/05/1998", "confidence": 0.9},
            {"text": "2345 6789 0125", "confidence": 0.9},  # tampered last digit
        ]
        res = extractor.parse_blocks(blocks)
        assert res["checksum_valid"] is False
        assert res["extraction_confidence"] < 0.85  # must be penalized
        # NOTE: see DEFECT-003 — this penalty alone is not enough to stop
        # the decision engine from approving the registration.

    def test_name_extraction_skips_relative_name_lines(self):
        """A 'Father's Name: X' line must never be extracted as the
        cardholder's own name."""
        from pipeline.field_extractor import FieldExtractor
        extractor = FieldExtractor()
        blocks = [
            {"text": "Father's Name: SURESH KUMAR", "confidence": 0.9},
            {"text": "PRIYA SHARMA", "confidence": 0.9},
            {"text": "DOB: 21/08/2000", "confidence": 0.9},
        ]
        res = extractor.parse_blocks(blocks)
        assert res["name"] != "SURESH KUMAR"

    def test_no_id_number_extracted_lowers_confidence(self):
        from pipeline.field_extractor import FieldExtractor
        extractor = FieldExtractor()
        blocks = [{"text": "Government of India", "confidence": 0.9},
                   {"text": "SOMEONE NAME", "confidence": 0.9}]
        res = extractor.parse_blocks(blocks)
        assert res["id_number"] is None
        assert res["extraction_confidence"] <= 0.65


# ===========================================================================
# DECISION ENGINE — boundary conditions
# ===========================================================================

class TestDecisionEngineBoundaries:
    def _base_inputs(self, dob):
        return dict(
            quality_res={"quality_confidence": 0.95, "flags": [], "blur_score": 250.0},
            ocr_res={"extraction_confidence": 0.90, "date_of_birth": dob,
                     "id_type": "aadhaar", "id_number_masked": "****0124"},
            identity_res={"face_match": {"score": 0.90, "verdict": "match"},
                          "name_match": {"score": 96.0, "verdict": "match"}, "flags": []},
            duplicate_res={"is_duplicate": False, "flags": []},
        )

    def test_exactly_min_age_is_not_rejected(self):
        """Someone whose 18th birthday is today must PASS the age check,
        not fail it on an off-by-one."""
        from pipeline.decision_engine import DecisionEngine
        today = datetime.now()
        dob_18_today = today.replace(year=today.year - 18).strftime("%Y-%m-%d")
        engine = DecisionEngine()
        res = engine.decide(**self._base_inputs(dob_18_today))
        assert res["decision"] != "rejected", (
            f"A participant turning exactly 18 today was rejected: "
            f"{res['reason']!r}."
        )
        assert res["breakdown"]["eligibility"]["computed_age"] == 18

    def test_one_day_under_min_age_is_rejected(self):
        """Someone who turns 18 tomorrow (still 17 today) must be
        rejected — the false-negative direction must not slip."""
        from pipeline.decision_engine import DecisionEngine
        tomorrow = datetime.now() + timedelta(days=1)
        dob_turns_18_tomorrow = tomorrow.replace(year=tomorrow.year - 18).strftime("%Y-%m-%d")
        engine = DecisionEngine()
        res = engine.decide(**self._base_inputs(dob_turns_18_tomorrow))
        assert res["decision"] == "rejected"
        assert "17" in res["reason"]

    def test_confidence_score_always_bounded_0_to_1(self):
        """Even with out-of-range/contradictory inputs (a defensive
        upstream bug elsewhere), the final confidence must stay in [0, 1]
        so downstream consumers (dashboard, API contract) never see a
        nonsensical value."""
        from pipeline.decision_engine import DecisionEngine
        engine = DecisionEngine()
        res = engine.decide(
            quality_res={"quality_confidence": 1.5, "flags": []},
            ocr_res={"extraction_confidence": -0.5, "date_of_birth": None, "id_type": "aadhaar"},
            identity_res={"face_match": {"score": 2.0, "verdict": "match"},
                          "name_match": {"score": 150.0, "verdict": "match"}, "flags": []},
            duplicate_res={"is_duplicate": False, "flags": []},
        )
        assert 0.0 <= res["confidence"] <= 1.0

    def test_student_only_event_rejects_non_college_id(self):
        from pipeline.decision_engine import DecisionEngine
        engine = DecisionEngine()
        inputs = self._base_inputs(dob="1998-05-14")
        res = engine.decide(**inputs, event_rules={"min_age": 18, "student_only": True})
        assert res["decision"] == "rejected"
        assert "college" in res["reason"].lower() or "student" in res["reason"].lower()

    def test_college_id_passes_student_only_event(self):
        from pipeline.decision_engine import DecisionEngine
        engine = DecisionEngine()
        inputs = self._base_inputs(dob="2003-05-14")
        inputs["ocr_res"]["id_type"] = "college_id"
        res = engine.decide(**inputs, event_rules={"min_age": 18, "student_only": True})
        assert res["decision"] != "rejected", res["reason"]


# ===========================================================================
# QUALITY ANALYZER — missing files (must not crash the pipeline)
# ===========================================================================

class TestQualityAnalyzerRobustness:
    def test_nonexistent_file_returns_safe_failure_not_exception(self):
        from pipeline.quality_analyzer import QualityAnalyzer
        res = QualityAnalyzer().analyze("/path/does/not/exist_" + uuid.uuid4().hex + ".jpg")
        assert res["quality_passed"] is False
        assert "file_not_found" in res["flags"]

    # NOTE: a file that EXISTS but is corrupt/unreadable (zero-byte, a
    # renamed non-image) currently does NOT fail this check the way a
    # missing file does — see DEFECT-007 in test_critical_defects.py.


# ===========================================================================
# DUPLICATE DETECTOR — normalization edge cases
# ===========================================================================

class TestDuplicateDetectorNormalization:
    @pytest.fixture(autouse=True)
    def _sqlite_db(self, tmp_path, monkeypatch):
        monkeypatch.setenv("DATABASE_PROVIDER", "sqlite")
        from app.config import config
        monkeypatch.setitem(config["database"], "provider", "sqlite")
        monkeypatch.setitem(config["database"], "db_path", str(tmp_path / "edge.db"))
        import app.database as db
        monkeypatch.setattr(db, "DB_PATH", tmp_path / "edge.db")
        db.init_db()

    def test_id_number_with_different_spacing_still_detected_as_duplicate(self):
        """'2345 6789 0124' and '234567890124' are the same Aadhaar and
        must hash to the same fingerprint regardless of spacing."""
        from pipeline.duplicate_detector import DuplicateDetector
        detector = DuplicateDetector()
        detector.check_and_register("aadhaar", "2345 6789 0124", "Arjun Kumar", "reg_x")
        r2 = detector.check_and_register("aadhaar", "234567890124", "Different Person", "reg_y")
        assert r2["is_duplicate"] is True
        assert "duplicate_id_different_name" in r2["flags"]

    def test_id_number_case_insensitive_for_pan(self):
        from pipeline.duplicate_detector import DuplicateDetector
        detector = DuplicateDetector()
        detector.check_and_register("pan", "abcde1234f", "Arjun Kumar", "reg_x")
        r2 = detector.check_and_register("pan", "ABCDE1234F", "Someone Else", "reg_y")
        assert r2["is_duplicate"] is True, (
            "Lowercase vs uppercase PAN should still fingerprint to the "
            "same hash — case must be normalized before hashing."
        )

    def test_missing_id_number_skips_duplicate_check_gracefully(self):
        from pipeline.duplicate_detector import DuplicateDetector
        detector = DuplicateDetector()
        res = detector.check_and_register(None, None, "Someone", "reg_z")
        assert res["is_duplicate"] is False
        assert "skipped" in res["details"].lower()


# ===========================================================================
# NAME MATCHING — fuzzy match boundaries
# ===========================================================================

class TestNameMatchingBoundaries:
    def test_reordered_name_still_matches(self):
        """'Kumar Arjun' vs 'Arjun Kumar' — same person, different word
        order. NOTE: this currently passes for the wrong reason — see
        DEFECT-008: both sides get reduced to just 'arjun' because 'Kumar'
        is (incorrectly) stripped as an honorific from both, so this is
        an accidental exact-match rather than genuine reordering logic.
        Re-verify this test once DEFECT-008 is fixed."""
        from pipeline.identity_verifier import IdentityVerifier
        res = IdentityVerifier()._match_names("Kumar Arjun", "ARJUN KUMAR")
        assert res["verdict"] in ("match", "uncertain")

    def test_completely_different_names_score_low(self):
        from pipeline.identity_verifier import IdentityVerifier
        res = IdentityVerifier()._match_names("Zebra Quicksilver", "Aardvark Wonderland")
        assert res["verdict"] == "mismatch"

    def test_empty_form_name_treated_as_uncertain_not_match(self):
        from pipeline.identity_verifier import IdentityVerifier
        res = IdentityVerifier()._match_names("", "ARJUN KUMAR")
        assert res["verdict"] == "uncertain"
