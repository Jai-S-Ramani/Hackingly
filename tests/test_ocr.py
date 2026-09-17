import pytest
from pipeline.field_extractor import FieldExtractor, validate_verhoeff_aadhaar, mask_id_number

def test_verhoeff_checksum_algorithm():
    # Valid Aadhaar numbers generated via Verhoeff checksum
    # Example valid: 2345 6789 0124
    assert validate_verhoeff_aadhaar("234567890124") is True
    # Tampered last digit
    assert validate_verhoeff_aadhaar("234567890125") is False

def test_mask_id_number():
    assert mask_id_number("1234 5678 9012") == "****9012"
    assert mask_id_number("ABCDE1234F") == "****234F"

def test_field_extraction_aadhaar():
    extractor = FieldExtractor()
    sample_blocks = [
        {"text": "Government of India", "confidence": 0.95},
        {"text": "ARJUN KUMAR", "confidence": 0.90},
        {"text": "DOB: 14/05/1998", "confidence": 0.92},
        {"text": "2345 6789 0124", "confidence": 0.96}
    ]
    res = extractor.parse_blocks(sample_blocks)
    assert res["id_type"] == "aadhaar"
    assert res["date_of_birth"] == "1998-05-14"
    assert res["id_number"] == "2345 6789 0124"
    assert res["name"] == "ARJUN KUMAR"
    assert res["checksum_valid"] is True

def test_field_extraction_pan():
    extractor = FieldExtractor()
    sample_blocks = [
        {"text": "INCOME TAX DEPARTMENT", "confidence": 0.95},
        {"text": "PRIYA SHARMA", "confidence": 0.91},
        {"text": "21/08/2000", "confidence": 0.90},
        {"text": "ABCDE1234F", "confidence": 0.97}
    ]
    res = extractor.parse_blocks(sample_blocks)
    assert res["id_type"] == "pan"
    assert res["id_number"] == "ABCDE1234F"
    assert res["format_valid"] is True
