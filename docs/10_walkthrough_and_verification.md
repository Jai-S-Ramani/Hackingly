# VerifyAI — Build Walkthrough & Verification

All 5 core modules, API routes, database schemas, sample generation scripts, and test suites have been implemented and verified.

---

## 1. Project Implementation Overview

```
E:\Hackingly\
├── app/
│   ├── config.py                 # YAML configuration loader with defaults
│   ├── database.py               # SQLite schema (events, registrations, verifications, id_hashes)
│   ├── models.py                 # Pydantic models for API request/response validation
│   ├── main.py                   # FastAPI app with CORS & lifespan initialization
│   └── routes/
│       ├── health.py             # GET /api/v1/health
│       ├── verify.py             # POST /api/v1/verify (Multipart upload & execution)
│       └── registrations.py      # GET /api/v1/registrations, override, POST /events
├── pipeline/
│   ├── quality_analyzer.py       # [Member 3] Laplacian blur, ELA tampering, EXIF forensics
│   ├── ocr_adapter.py            # [Member 2] Pluggable OCR interface (EasyOCR, Textract, Mock)
│   ├── field_extractor.py        # [Member 2] Verhoeff checksum algorithm, PAN regex, DOB parser
│   ├── identity_verifier.py      # [Member 4] DeepFace face matcher & RapidFuzz name matcher
│   ├── duplicate_detector.py     # [Member 1] SHA-256 fingerprint & SQLite cross-name reuse check
│   ├── decision_engine.py        # [Member 5] Weighted scoring, age check, plain-English reasons
│   └── orchestrator.py           # [Member 1] Pipeline coordinator (Stages 1 -> 5)
├── dashboard/
│   └── app.py                    # [Member 5] Streamlit organizer dashboard with live test sandbox
├── tests/
│   ├── test_quality.py           # Stage 1 tests (Laplacian blur & sharpness)
│   ├── test_ocr.py               # Stage 2 tests (Verhoeff checksum, PAN regex, field parsing)
│   ├── test_identity.py          # Stage 3 tests (Name fuzzy matching & biometrics)
│   ├── test_duplicates.py        # Stage 4 tests (Cross-name fraud prevention)
│   ├── test_decision.py          # Stage 5 tests (Approval, Underage reject, Duplicate reject)
│   └── test_e2e.py               # Full API end-to-end multipart pipeline test
├── scripts/
│   └── generate_samples.py       # Generates synthetic Aadhaar, PAN, blurry ID, selfie
├── data/
│   └── samples/                  # Generated test image samples
├── config.yaml                   # Global configuration thresholds
└── requirements.txt              # All dependencies
```

---

## 2. Test Execution & Verification

Ran pytest across all unit and integration test suites:
```bash
python -m pytest tests/ -v
```

### Results
```
============================= test session starts =============================
platform win32 -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0 -- C:\Python314\python.exe
cachedir: .pytest_cache
rootdir: E:\Hackingly
plugins: anyio-4.14.2, shiny-1.7.0
collecting ... collected 17 items

tests/test_decision.py::test_clean_application_approved PASSED           [  5%]
tests/test_decision.py::test_duplicate_id_rejected PASSED                [ 11%]
tests/test_decision.py::test_underage_rejected PASSED                    [ 17%]
tests/test_duplicates.py::test_duplicate_different_name_flagged PASSED   [ 23%]
tests/test_e2e.py::test_health_endpoint PASSED                           [ 29%]
tests/test_e2e.py::test_verify_pipeline_e2e PASSED                       [ 35%]
tests/test_e2e.py::test_registrations_listing PASSED                     [ 41%]
tests/test_identity.py::test_name_exact_match PASSED                     [ 47%]
tests/test_identity.py::test_name_honorific_match PASSED                 [ 52%]
tests/test_identity.py::test_name_mismatch PASSED                        [ 58%]
tests/test_identity.py::test_no_selfie_graceful PASSED                   [ 64%]
tests/test_ocr.py::test_verhoeff_checksum_algorithm PASSED               [ 70%]
tests/test_ocr.py::test_mask_id_number PASSED                            [ 76%]
tests/test_ocr.py::test_field_extraction_aadhaar PASSED                  [ 82%]
tests/test_ocr.py::test_field_extraction_pan PASSED                      [ 88%]
tests/test_quality.py::test_sharp_image_passes PASSED                    [ 94%]
tests/test_quality.py::test_blurry_image_fails_or_flags PASSED           [100%]

============================= 17 passed in 0.72s ==============================
```

---

## 3. How the Team Can Run and Demo the Solution

### Step 1: Start the Backend API Server
```powershell
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- Interactive Swagger docs will be live at: `http://localhost:8000/docs`

### Step 2: Start the Organizer Dashboard
```powershell
python -m streamlit run dashboard/app.py
```
- Organizer dashboard UI will open at: `http://localhost:8501`

### Step 3: Run Live Verifications
In the Streamlit dashboard or via cURL:
```powershell
curl -X POST http://localhost:8000/api/v1/verify `
  -F "id_image=@data/samples/valid_aadhaar.jpg" `
  -F "selfie=@data/samples/sample_selfie.jpg" `
  -F "form_name=Arjun Kumar" `
  -F "form_email=arjun.kumar@example.com" `
  -F "form_dob=1998-05-14" `
  -F "event_id=hackathon-2026"
```
