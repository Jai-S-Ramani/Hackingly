# 🛡️ VerifyAI
### AI-Powered Identity & Eligibility Verification for Hackathon Registrations

> **PS-003** · AI Build Challenge — Bengaluru · Powered by Hackingly

---

## ✨ What It Does

VerifyAI transforms Hackingly's basic OCR-based DOB extraction into a **comprehensive identity verification pipeline** that can:

| Capability | How |
|---|---|
| 📄 **Extract ID fields** | Name, DOB, ID number, ID type from Aadhaar, PAN, College IDs |
| 🔍 **Detect fake documents** | Error Level Analysis (ELA) + EXIF metadata forensics |
| 👤 **Verify identity** | Face match (selfie vs. ID photo) + name cross-check |
| 🔁 **Catch duplicate IDs** | Same ID reused under different names → flagged |
| ✅ **Decide eligibility** | Confidence score + human-readable reason per registration |

**One upload. One selfie. Instant verification.**

---

## 🏗️ Architecture

```
Upload → Quality Check → OCR → Identity Match → Duplicate Check → Decision
         (OpenCV)     (EasyOCR)  (DeepFace)      (SQLite)        (Rules)
```

- **100% open-source** processing pipeline
- **Pluggable OCR adapter** — swap EasyOCR ↔ PaddleOCR ↔ AWS Textract via config
- **FastAPI** backend + **Streamlit** organizer dashboard
- **SQLite** for lightweight persistence

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation
```bash
# Clone the repository
git clone <repo-url>
cd verifyai

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app.database import init_db; init_db()"
```

### Run the API Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Run the Organizer Dashboard
```bash
streamlit run dashboard/app.py
```

### Verify a Registration
```bash
curl -X POST http://localhost:8000/api/v1/verify \
  -F "id_image=@sample_aadhaar.jpg" \
  -F "selfie=@selfie.jpg" \
  -F "form_name=Arjun Kumar" \
  -F "event_id=hackathon-2026"
```

### Response
```json
{
  "decision": "approved",
  "confidence": 0.87,
  "reason": "All checks passed. Identity verified with high confidence."
}
```

---

## 📁 Project Structure

```
verifyai/
├── app/                     # FastAPI application
│   ├── main.py              # Entry point
│   ├── config.py            # Configuration
│   ├── models.py            # Request/response schemas
│   ├── database.py          # SQLite setup
│   └── routes/              # API endpoints
├── pipeline/                # Verification pipeline
│   ├── orchestrator.py      # Pipeline coordinator
│   ├── quality_analyzer.py  # Blur, tampering, quality
│   ├── ocr_adapter.py       # Pluggable OCR (EasyOCR/Textract)
│   ├── field_extractor.py   # Name, DOB, ID parsing
│   ├── identity_verifier.py # Face + name matching
│   ├── duplicate_detector.py# Duplicate ID detection
│   └── decision_engine.py   # Final eligibility decision
├── dashboard/               # Streamlit organizer UI
├── tests/                   # Test suite
├── config.yaml              # Runtime configuration
└── requirements.txt         # Dependencies
```

---

## 🔧 Configuration

Edit `config.yaml` to switch OCR engines, adjust thresholds, or change decision weights:

```yaml
ocr:
  engine: "easyocr"      # easyocr | paddleocr | textract

face_match:
  threshold_match: 0.60  # Above = match
  threshold_uncertain: 0.40  # Below = mismatch

decision:
  approve_threshold: 0.75
  review_threshold: 0.50
```

---

## 🧰 Tech Stack

| Component | Tool | License |
|---|---|---|
| API | FastAPI | MIT |
| OCR | EasyOCR / PaddleOCR | Apache 2.0 |
| Face Match | DeepFace (ArcFace) | MIT |
| Name Match | RapidFuzz | MIT |
| Tampering | OpenCV + Pillow | Apache 2.0 / BSD |
| Database | SQLite | Public Domain |
| Dashboard | Streamlit | Apache 2.0 |

---

## 📊 Performance

| Metric | Target |
|---|---|
| End-to-end latency | < 8 seconds |
| Face match accuracy | > 95% |
| OCR accuracy | > 90% |
| False positive rate | < 2% |

---

## 🔒 Privacy

- Face embeddings are **never stored** — computed in-memory, discarded after comparison
- Full ID numbers are **never stored** — only a SHA-256 hash + last 4 digits
- Raw images are **deleted after processing**
- All processing is **local** — no external API calls (except org-provided Textract)

---

## 📝 License

Built for the AI Build Challenge — Bengaluru 2026.

---

*Built with ❤️ for Hackingly*
