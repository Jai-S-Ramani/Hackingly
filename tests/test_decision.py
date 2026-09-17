import pytest
from pipeline.decision_engine import DecisionEngine

def test_clean_application_approved():
    engine = DecisionEngine()
    quality_res = {"quality_confidence": 0.95, "flags": [], "blur_score": 250.0}
    ocr_res = {"extraction_confidence": 0.90, "date_of_birth": "1998-05-14", "id_type": "aadhaar", "id_number_masked": "****6012"}
    identity_res = {"face_match": {"score": 0.85, "verdict": "match"}, "name_match": {"score": 95.0, "verdict": "match"}, "flags": []}
    duplicate_res = {"is_duplicate": False, "flags": []}

    res = engine.decide(quality_res, ocr_res, identity_res, duplicate_res)
    assert res["decision"] == "approved"
    assert res["confidence"] >= 0.75
    assert "passed" in res["reason"].lower()

def test_duplicate_id_rejected():
    engine = DecisionEngine()
    quality_res = {"quality_confidence": 0.90, "flags": []}
    ocr_res = {"extraction_confidence": 0.90, "date_of_birth": "1998-05-14", "id_type": "aadhaar"}
    identity_res = {"face_match": {"score": 0.80}, "name_match": {"score": 90.0}, "flags": []}
    duplicate_res = {"is_duplicate": True, "flags": ["duplicate_id_different_name"]}

    res = engine.decide(quality_res, ocr_res, identity_res, duplicate_res)
    assert res["decision"] == "rejected"
    assert "duplicate" in res["reason"].lower()

def test_underage_rejected():
    engine = DecisionEngine()
    quality_res = {"quality_confidence": 0.90, "flags": []}
    # Age 14 (born 2012)
    ocr_res = {"extraction_confidence": 0.90, "date_of_birth": "2012-05-14", "id_type": "aadhaar"}
    identity_res = {"face_match": {"score": 0.80}, "name_match": {"score": 90.0}, "flags": []}
    duplicate_res = {"is_duplicate": False, "flags": []}

    res = engine.decide(quality_res, ocr_res, identity_res, duplicate_res, event_rules={"min_age": 18})
    assert res["decision"] == "rejected"
    assert "age" in res["reason"].lower()
