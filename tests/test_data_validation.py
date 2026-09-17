import os
import sqlite3
import cv2
import pytest
from pipeline.quality_analyzer import QualityAnalyzer
from pipeline.decision_engine import DecisionEngine

SAMPLES_DIR = "data/samples"
DB_PATH = "data/verifyai.db"

def test_all_sample_files_exist():
    expected_files = [
        "valid_aadhaar.jpg",
        "valid_pan.jpg",
        "valid_college_id.jpg",
        "valid_voter_id.jpg",
        "underage_id.jpg",
        "tampered_doc.jpg",
        "blurry_doc.jpg",
        "sample_selfie.jpg",
        "mismatch_selfie.jpg"
    ]
    for fname in expected_files:
        fpath = os.path.join(SAMPLES_DIR, fname)
        assert os.path.exists(fpath), f"Missing sample file: {fpath}"
        assert os.path.getsize(fpath) > 1000, f"Sample file {fpath} is empty or too small"

def test_sample_image_resolutions():
    for fname in os.listdir(SAMPLES_DIR):
        if not fname.endswith((".jpg", ".png")):
            continue
        img = cv2.imread(os.path.join(SAMPLES_DIR, fname))
        assert img is not None, f"Failed to read image {fname}"
        h, w = img.shape[:2]
        assert h >= 400, f"Height of {fname} ({h}) is less than 400"
        assert w >= 300, f"Width of {fname} ({w}) is less than 300"

def test_blurry_document_flagged():
    qa = QualityAnalyzer()
    res = qa.analyze(os.path.join(SAMPLES_DIR, "blurry_doc.jpg"))
    assert "blurry_image" in res["flags"]
    assert res["blur_score"] < 100.0

def test_tampered_document_ela_detection():
    qa = QualityAnalyzer()
    res = qa.analyze(os.path.join(SAMPLES_DIR, "tampered_doc.jpg"))
    assert res["tampering_score"] > 0.0
    assert res["ela_heatmap_base64"] is not None

def test_seeded_database_integrity():
    from app.database import get_supabase_client, is_supabase_active, get_all_registrations
    
    if is_supabase_active():
        client = get_supabase_client()
        res = client.table("registrations").select("id").execute()
        reg_count = len(res.data)
        assert reg_count >= 15, f"Expected at least 15 seeded registrations in Supabase, got {reg_count}"

        res_app = client.table("verifications").select("id").eq("decision", "approved").execute()
        assert len(res_app.data) >= 6, f"Expected at least 6 approved registrations in Supabase, got {len(res_app.data)}"

        res_rej = client.table("verifications").select("id").eq("decision", "rejected").execute()
        assert len(res_rej.data) >= 4, f"Expected at least 4 rejected registrations in Supabase, got {len(res_rej.data)}"

        res_rev = client.table("verifications").select("id").eq("decision", "manual_review").execute()
        assert len(res_rev.data) >= 2, f"Expected at least 2 manual review registrations in Supabase, got {len(res_rev.data)}"
    else:
        assert os.path.exists(DB_PATH), f"Database file {DB_PATH} not found"
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM registrations;")
        reg_count = cursor.fetchone()[0]
        assert reg_count >= 15, f"Expected at least 15 seeded registrations, got {reg_count}"
        conn.close()
