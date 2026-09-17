import pytest
import uuid
from pipeline.duplicate_detector import DuplicateDetector
from app.database import init_db

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

def test_duplicate_different_name_flagged():
    detector = DuplicateDetector()
    unique_pan = f"PAND{uuid.uuid4().hex[:4].upper()}K"

    # First registration by Arjun Kumar
    res1 = detector.check_and_register(
        id_type="pan",
        id_number=unique_pan,
        registrant_name="Arjun Kumar",
        registration_id="reg_001"
    )
    assert res1["is_duplicate"] is False

    # Second registration using SAME PAN but by DIFFERENT person (Rahul Verma) -> FRAUD
    res2 = detector.check_and_register(
        id_type="pan",
        id_number=unique_pan,
        registrant_name="Rahul Verma",
        registration_id="reg_002"
    )
    assert res2["is_duplicate"] is True
    assert "duplicate_id_different_name" in res2["flags"]

def test_second_entry_same_user_flagged():
    detector = DuplicateDetector()
    unique_aadhaar = f"2{uuid.uuid4().int % 100000000000:011d}"

    # First registration
    res1 = detector.check_and_register(
        id_type="aadhaar",
        id_number=unique_aadhaar,
        registrant_name="Priya Sharma",
        registration_id="reg_010"
    )
    assert res1["is_duplicate"] is False

    # Second registration by SAME person with SAME ID
    res2 = detector.check_and_register(
        id_type="aadhaar",
        id_number=unique_aadhaar,
        registrant_name="Priya Sharma",
        registration_id="reg_011"
    )
    assert res2["is_duplicate"] is True
    assert "user_already_registered" in res2["flags"]
    assert "User Already Entered" in res2["details"]
