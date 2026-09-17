import pytest
from pipeline.identity_verifier import IdentityVerifier

def test_name_exact_match():
    verifier = IdentityVerifier()
    res = verifier._match_names("Arjun Kumar", "ARJUN KUMAR")
    assert res["verdict"] == "match"
    assert res["score"] >= 90.0

def test_name_honorific_match():
    verifier = IdentityVerifier()
    # Form has "Mr. Arjun Kumar", ID has "Arjun Kumar"
    res = verifier._match_names("Mr. Arjun Kumar", "ARJUN KUMAR")
    assert res["verdict"] == "match"

def test_name_mismatch():
    verifier = IdentityVerifier()
    res = verifier._match_names("Priya Sharma", "ARJUN KUMAR")
    assert res["verdict"] == "mismatch"
    assert res["score"] < 60.0

def test_no_selfie_graceful():
    verifier = IdentityVerifier()
    res = verifier._match_faces("dummy_id.jpg", None)
    assert res["verdict"] == "no_selfie_provided"
    assert res["selfie_provided"] is False
