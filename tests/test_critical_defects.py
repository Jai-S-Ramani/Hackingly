"""
CONFIRMED DEFECTS — found and dynamically verified by executing the real
code in this repo on 2026-09-18 (not just reasoned about from reading it).

Every assertion below was checked against the actual pipeline modules using
a lightweight harness (numpy/opencv/pillow/pyyaml only — no
easyocr/deepface/supabase/fastapi needed to reach any of these code paths).
Exact repro commands are in QA_TEST_REPORT.md.

Each test is marked `xfail(strict=True)`:
  - The assertion states the CORRECT/expected behavior.
  - It currently FAILS against the real code (confirmed by running it).
  - `strict=True` means: once someone fixes the bug, this test XPASSes and
    pytest treats that as a failure too — forcing you to notice and delete
    the xfail mark rather than the fix silently losing its regression test.

When a defect below is fixed:
  1. Delete its `@pytest.mark.xfail(...)` wrapper.
  2. Move the test body into the relevant test_*.py file.
  3. Update QA_TEST_REPORT.md's status column to "Fixed".
"""
import os
import sys
import tempfile
import uuid

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _xfail(reason):
    # Defect fixed — now active permanent regression test
    return lambda f: f


# ---------------------------------------------------------------------------
# DEFECT-001  [BLOCKER]  pipeline/field_extractor.py — NameError on import
# ---------------------------------------------------------------------------
# `Tuple` is used in `_extract_dob`'s return type hint but never imported
# (only List, Dict, Any, Optional are imported from typing). There's no
# `from __future__ import annotations`, so Python evaluates the annotation
# at function-definition time and raises NameError.
#
# BLAST RADIUS: pipeline/orchestrator.py imports field_extractor, and
# app/routes/verify.py imports orchestrator, and app/main.py imports that
# router. So this one missing import currently breaks collection of BOTH
# tests/test_ocr.py (direct import) AND tests/test_e2e.py (via the FastAPI
# app import chain) — the whole test suite is not "green minus a few edge
# cases", two entire modules can't even be collected right now.
@_xfail("field_extractor.py uses `Tuple` in a type hint without importing "
        "it, raising NameError on import and taking down "
        "tests/test_ocr.py and tests/test_e2e.py with it.")
def test_DEFECT_001_field_extractor_module_imports_cleanly():
    sys.modules.pop("pipeline.field_extractor", None)
    try:
        import pipeline.field_extractor  # noqa: F401
    except NameError as e:
        pytest.fail(
            f"pipeline/field_extractor.py fails to import: {e}. "
            f"Fix: add `Tuple` to the `from typing import ...` line."
        )


# ---------------------------------------------------------------------------
# DEFECT-002  [CRITICAL]  pipeline/identity_verifier.py — fail-open face match
# ---------------------------------------------------------------------------
# `_match_faces` wraps the DeepFace call in a bare `except Exception`, and
# on ANY failure (missing model weights, no internet at the venue, corrupt
# image, non-image bytes, DeepFace not installed...) it returns a
# HARDCODED score of 0.88 and verdict "match". A processing failure
# silently reports a false-positive "match" instead of surfacing the
# error — the opposite of what a verification system should do.
@_xfail("identity_verifier._match_faces silently returns score=0.88 "
        "verdict='match' on ANY exception instead of failing closed.")
def test_DEFECT_002_face_match_fails_closed_not_open():
    from pipeline.identity_verifier import IdentityVerifier

    p1 = os.path.join(tempfile.gettempdir(), f"defect002_id_{uuid.uuid4().hex}.jpg")
    p2 = os.path.join(tempfile.gettempdir(), f"defect002_selfie_{uuid.uuid4().hex}.jpg")
    with open(p1, "wb") as f:
        f.write(b"this is not an image")
    with open(p2, "wb") as f:
        f.write(b"neither is this")

    try:
        result = IdentityVerifier()._match_faces(p1, p2)
        assert result["verdict"] in ("error", "uncertain", "no_selfie_provided"), (
            f"Face match returned verdict={result['verdict']!r} with a "
            f"fabricated score of {result.get('score')} when the underlying "
            f"comparison could not actually run. Fix: on exception, return "
            f"verdict='error' (routed to manual_review), never a hardcoded "
            f"'match'."
        )
    finally:
        for p in (p1, p2):
            if os.path.exists(p):
                os.remove(p)


# ---------------------------------------------------------------------------
# DEFECT-003  [CRITICAL]  pipeline/decision_engine.py — checksum_valid ignored
# ---------------------------------------------------------------------------
# field_extractor computes `checksum_valid` (Verhoeff algorithm) and
# correctly detects a mathematically-invalid (i.e. very likely fabricated)
# Aadhaar number. decision_engine never reads this field and never adds a
# flag for it — it's only folded into extraction_confidence at OCR's 0.20
# weight, nowhere near enough to stop an otherwise-strong registration
# from auto-approving.
@_xfail("decision_engine never inspects ocr_res['checksum_valid']; a "
        "provably-fake Aadhaar number can still be auto-approved.")
def test_DEFECT_003_invalid_aadhaar_checksum_blocks_approval():
    from pipeline.decision_engine import DecisionEngine

    engine = DecisionEngine()
    quality_res = {"quality_confidence": 0.95, "flags": [], "blur_score": 250.0}
    ocr_res = {
        "extraction_confidence": 0.55,
        "date_of_birth": "1998-05-14",
        "id_type": "aadhaar",
        "id_number_masked": "****9999",
        "checksum_valid": False,  # fails Verhoeff: not a mathematically valid Aadhaar
        "format_valid": True,
    }
    identity_res = {
        "face_match": {"score": 0.95, "verdict": "match"},
        "name_match": {"score": 98.0, "verdict": "match"},
        "flags": [],
    }
    duplicate_res = {"is_duplicate": False, "flags": []}

    res = engine.decide(quality_res, ocr_res, identity_res, duplicate_res)
    assert res["decision"] != "approved", (
        f"A document whose ID number fails the Verhoeff checksum was "
        f"auto-APPROVED with confidence={res['confidence']}, flags={res['flags']}. "
        f"Fix: check ocr_res.get('checksum_valid') is False and hard-reject "
        f"or force manual_review with an 'invalid_id_checksum' flag."
    )


# ---------------------------------------------------------------------------
# DEFECT-004  [HIGH]  pipeline/duplicate_detector.py — cross-event false positive
# ---------------------------------------------------------------------------
# The ID fingerprint hash is sha256(f"{id_type}:{clean_id}") with no
# event_id folded in, and lookup_id_hashes() queries across ALL events. A
# legitimate participant registering for two different events with their
# own real ID gets rejected as "already registered" on the second event —
# guaranteed for any organizer (like Hackingly) running multiple events.
@_xfail("duplicate_detector hashes are not scoped by event_id, so the "
        "same legitimate person/ID is blocked across unrelated events.")
def test_DEFECT_004_same_person_same_id_different_events_not_blocked(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_PROVIDER", "sqlite")
    from app.config import config
    monkeypatch.setitem(config["database"], "provider", "sqlite")
    monkeypatch.setitem(config["database"], "db_path", str(tmp_path / "defect004.db"))

    import app.database as db
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "defect004.db")
    db.init_db()

    from pipeline.duplicate_detector import DuplicateDetector
    detector = DuplicateDetector()

    aadhaar = "234567890124"  # valid Verhoeff checksum
    r1 = detector.check_and_register(
        "aadhaar", aadhaar, "Arjun Kumar", "reg_evt_a", event_id="hackathon-2026"
    )
    assert r1["is_duplicate"] is False

    r2 = detector.check_and_register(
        "aadhaar", aadhaar, "Arjun Kumar", "reg_evt_b", event_id="totally-different-event-2027"
    )
    assert r2["is_duplicate"] is False, (
        f"The SAME real person used their OWN valid Aadhaar to register for "
        f"a DIFFERENT event and was flagged: flags={r2['flags']!r}. Fix: "
        f"scope the fingerprint/lookup by event_id, unless cross-event "
        f"blocking is a deliberate, documented product rule."
    )


# ---------------------------------------------------------------------------
# DEFECT-005  [HIGH]  pipeline/duplicate_detector.py — substring name match
# ---------------------------------------------------------------------------
# "same_person" is decided with `clean_name in n or n in clean_name` (raw
# substring containment). Any short/partial name is a substring of many
# longer names, so a genuine impersonation (different person reusing
# someone else's ID) can be misclassified as "the same user re-
# registering" — silently swallowing the exact fraud case the problem
# statement asks the system to catch.
@_xfail("duplicate_detector's same-person check uses substring "
        "containment, letting short-name impersonation slip through as a "
        "false 'same user' match instead of flagged fraud.")
def test_DEFECT_005_partial_name_reuse_flagged_as_fraud_not_resubmission(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_PROVIDER", "sqlite")
    from app.config import config
    monkeypatch.setitem(config["database"], "provider", "sqlite")
    monkeypatch.setitem(config["database"], "db_path", str(tmp_path / "defect005.db"))

    import app.database as db
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "defect005.db")
    db.init_db()

    from pipeline.duplicate_detector import DuplicateDetector
    detector = DuplicateDetector()

    pan = "ABCDE1234F"
    r1 = detector.check_and_register("pan", pan, "Ram", "reg_a", event_id="hackathon-2026")
    assert r1["is_duplicate"] is False

    # "ram" is a substring of "ramesh kumar" -> misread as the same person.
    r2 = detector.check_and_register(
        "pan", pan, "Ramesh Kumar", "reg_b", event_id="hackathon-2026"
    )
    assert "duplicate_id_different_name" in r2["flags"], (
        f"'Ramesh Kumar' reused 'Ram''s PAN and was classified as "
        f"flags={r2['flags']!r} (same person re-registering) instead of "
        f"'duplicate_id_different_name' (impersonation fraud). Fix: use "
        f"fuzzy token-set matching with a real similarity threshold "
        f"instead of raw substring containment."
    )


# ---------------------------------------------------------------------------
# DEFECT-006  [CRITICAL]  pipeline/decision_engine.py — missing DOB still approves
# ---------------------------------------------------------------------------
# When OCR can't read a date of birth at all, `age_passed` defaults to
# True and NO flag is ever added for "age could not be verified". If every
# other signal looks fine, the registration is auto-approved with the
# reason "All checks passed successfully" — even though the single most
# important eligibility check (age) was never actually performed. This is
# a silent bypass of the primary eligibility gate the problem statement
# asks for.
@_xfail("decision_engine treats an unreadable/missing DOB as "
        "age_passed=True with no flag, so age-gated events can "
        "auto-approve someone whose age was never verified at all.")
def test_DEFECT_006_missing_dob_never_auto_approves():
    from pipeline.decision_engine import DecisionEngine

    engine = DecisionEngine()
    res = engine.decide(
        quality_res={"quality_confidence": 0.95, "flags": [], "blur_score": 250.0},
        ocr_res={"extraction_confidence": 0.40, "date_of_birth": None,
                 "id_type": "aadhaar", "id_number_masked": "****0124"},
        identity_res={"face_match": {"score": 0.90, "verdict": "match"},
                      "name_match": {"score": 96.0, "verdict": "match"}, "flags": []},
        duplicate_res={"is_duplicate": False, "flags": []},
    )
    assert res["decision"] != "approved", (
        f"A registration with NO extracted date of birth was APPROVED "
        f"(confidence={res['confidence']}, reason={res['reason']!r}). Age "
        f"eligibility — the core requirement of this problem statement — "
        f"was never actually checked. Fix: when date_of_birth is None, add "
        f"an explicit 'age_unverified' flag and route to manual_review "
        f"(or reject), never approve."
    )


# ---------------------------------------------------------------------------
# DEFECT-007  [CRITICAL]  pipeline/quality_analyzer.py — corrupt file passes
# ---------------------------------------------------------------------------
# When cv2/PIL can't even open the file (corrupt image, a renamed non-image
# file, a zero-byte file), the exception handlers append messages like
# "quality_cv_error: ..." / "quality_ela_error: ..." to `flags` — but
# `quality_passed` only checks for the literal strings "blurry_image",
# "low_resolution", "potential_tampering_ela". None of those match, so
# `quality_passed` computes to True for a file that could not be read at
# all. Combined with DEFECT-002 (face match fails open), a completely
# non-image upload can sail through both the quality gate and the face
# match gate.
@_xfail("quality_analyzer.analyze() reports quality_passed=True for a "
        "file that could not even be opened/decoded as an image — the "
        "cv/ela error flags don't match the literal strings checked by "
        "the quality_passed calculation.")
def test_DEFECT_007_unreadable_file_fails_quality_check():
    from pipeline.quality_analyzer import QualityAnalyzer

    path = os.path.join(tempfile.gettempdir(), f"corrupt_{uuid.uuid4().hex}.jpg")
    with open(path, "wb") as f:
        f.write(b"%PDF-1.4 this is not actually a jpeg")
    try:
        res = QualityAnalyzer().analyze(path)
        assert res["quality_passed"] is False, (
            f"A non-image file (renamed .pdf) that cv2/PIL could not even "
            f"decode was reported as quality_passed=True with flags="
            f"{res['flags']!r}. Fix: if the cv2/PIL decode step raises, "
            f"quality_passed must be forced to False regardless of the "
            f"specific error-flag strings."
        )
    finally:
        os.remove(path)


# ---------------------------------------------------------------------------
# DEFECT-008  [CRITICAL]  pipeline/identity_verifier.py — "Kumar"/"Kumari"
#                          stripped as an honorific
# ---------------------------------------------------------------------------
# `_normalize_name` strips a hardcoded honorific list that includes
# "kumar" and "kumari" before any name comparison happens. "Kumar" is
# overwhelmingly used as an actual SURNAME by a very large share of Indian
# ID holders (the exact population this system verifies), not as an
# honorific/title like "Mr"/"Dr"/"Shri". This silently deletes real,
# load-bearing identity information from both the form name and the
# extracted ID name before every single name-match comparison —
# regardless of whether rapidfuzz or the offline fallback scorer is used,
# since the stripping happens upstream of both.
@_xfail("identity_verifier._normalize_name treats 'kumar'/'kumari' as "
        "honorifics and strips them, discarding a common real Indian "
        "surname from every name-match comparison.")
def test_DEFECT_008_kumar_surname_not_stripped_as_honorific():
    from pipeline.identity_verifier import IdentityVerifier

    verifier = IdentityVerifier()
    normalized = verifier._normalize_name("Arjun Kumar")
    assert "kumar" in normalized, (
        f"_normalize_name('Arjun Kumar') returned {normalized!r} — the "
        f"surname 'Kumar' was deleted entirely, as if it were a title "
        f"like 'Mr' or 'Dr'. This affects every name-match comparison for "
        f"the huge share of Indian ID holders who carry 'Kumar'/'Kumari' "
        f"as their actual surname. Fix: remove 'kumar'/'kumari' from the "
        f"honorific-stripping regex."
    )
