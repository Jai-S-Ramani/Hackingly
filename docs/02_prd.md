# Product Requirements Document (PRD)
## VerifyAI — AI-Powered Identity & Eligibility Verification for Hackingly

| Field | Detail |
|---|---|
| **Product Name** | VerifyAI |
| **Version** | 1.0 |
| **Date** | 17 September 2026 |
| **Event** | AI Build Challenge — Bengaluru, 18 Sept 2026 |
| **Problem Statement** | PS-003 |
| **Industry Partner** | Hackingly |

---

## 1. Executive Summary

**VerifyAI** is an AI-powered identity and eligibility verification system that extends Hackingly's existing registration pipeline. It transforms a basic OCR-based DOB extraction into a comprehensive verification engine that can detect fake/tampered documents, catch duplicate IDs, verify identity through face matching, and deliver confidence-scored eligibility decisions — all built on open-source tools.

### 1.1 Problem Statement

Hackingly runs registrations for hackathons and competitions that are often age-restricted, student-only, or ID-gated. The current system:
- Extracts only DOB via AWS Textract for age checks
- Cannot detect fake, tampered, or edited documents
- Cannot catch the same ID reused across multiple registrations
- Cannot confirm the person registering matches the ID submitted
- Requires manual verification that doesn't scale

### 1.2 Product Vision

> **One upload. One selfie. Instant, trustworthy verification.**

Replace hours of manual document review with a sub-10-second automated pipeline that gives organizers a clear decision, a confidence score, and a human-readable reason for every registration.

---

## 2. User Personas

### 2.1 Primary: Hackathon Organizer (Riya)
- **Role**: Event organizer using Hackingly's platform
- **Goal**: Verify 500+ registrations quickly without manually checking each ID
- **Pain Point**: Spends 2–3 hours per event reviewing uploaded IDs, still misses fakes
- **Need**: Dashboard showing verified/flagged/rejected registrations with actionable reasons

### 2.2 Primary: Hackathon Participant (Arjun)
- **Role**: Student registering for a hackathon
- **Goal**: Register quickly without being blocked by false verification failures
- **Pain Point**: Gets frustrated when legitimate uploads are flagged as invalid
- **Need**: Clear feedback if an upload fails, with guidance to fix it (e.g., "Image too blurry, please re-upload")

### 2.3 Secondary: Hackingly Platform Admin (Dev Team)
- **Role**: Technical team maintaining the registration pipeline
- **Goal**: Integrate verification with minimal changes to the existing flow
- **Need**: Clean API, pluggable architecture, minimal infrastructure changes

---

## 3. Functional Requirements

### FR-1: Document Upload & Quality Check
| ID | Requirement | Priority |
|---|---|---|
| FR-1.1 | Accept image uploads (JPEG, PNG, WebP) of ID documents | P0 |
| FR-1.2 | Accept selfie photo upload | P0 |
| FR-1.3 | Detect and reject blurry images (Laplacian variance < threshold) | P0 |
| FR-1.4 | Detect and reject images below minimum resolution (300×400 px) | P0 |
| FR-1.5 | Return actionable feedback for rejected uploads (reason + guidance) | P1 |

### FR-2: Document Tampering Detection
| ID | Requirement | Priority |
|---|---|---|
| FR-2.1 | Perform Error Level Analysis (ELA) to detect edited regions | P0 |
| FR-2.2 | Check EXIF metadata for editing software signatures | P1 |
| FR-2.3 | Flag documents with tampering confidence > threshold | P0 |
| FR-2.4 | Return tampered regions/reasons in the verification response | P1 |

### FR-3: OCR & Field Extraction
| ID | Requirement | Priority |
|---|---|---|
| FR-3.1 | Extract **name** from uploaded ID | P0 |
| FR-3.2 | Extract **date of birth** from uploaded ID | P0 |
| FR-3.3 | Extract **ID number** (Aadhaar no., PAN no., roll no.) from uploaded ID | P0 |
| FR-3.4 | Extract **ID type** (classify: Aadhaar, PAN, College ID, etc.) | P0 |
| FR-3.5 | Extract **institution name** from college IDs | P1 |
| FR-3.6 | Validate Aadhaar number using Verhoeff checksum | P1 |
| FR-3.7 | Validate PAN format (ABCDE1234F regex) | P1 |
| FR-3.8 | Support English and Hindi text extraction | P1 |
| FR-3.9 | Pluggable OCR backend (EasyOCR default, Textract swappable) | P0 |

### FR-4: Identity Verification
| ID | Requirement | Priority |
|---|---|---|
| FR-4.1 | Compare selfie photo with ID document photo using face embeddings | P0 |
| FR-4.2 | Return face match similarity score (0.0–1.0) | P0 |
| FR-4.3 | Fuzzy-match extracted name against registration form name | P0 |
| FR-4.4 | Handle Hindi↔English name transliteration for matching | P2 |
| FR-4.5 | Gracefully degrade if selfie is not provided (lower confidence, no hard reject) | P1 |

### FR-5: Duplicate Detection
| ID | Requirement | Priority |
|---|---|---|
| FR-5.1 | Store hash of (ID type + ID number) for each processed registration | P0 |
| FR-5.2 | Flag if the same ID number appears under a different registrant name | P0 |
| FR-5.3 | Flag fuzzy duplicates (similar name + similar DOB across registrations) | P2 |
| FR-5.4 | Support cross-event duplicate detection | P2 |

### FR-6: Eligibility Decision Engine
| ID | Requirement | Priority |
|---|---|---|
| FR-6.1 | Apply configurable event rules (min age, max age, student-only, etc.) | P0 |
| FR-6.2 | Output three-tier decision: `approved` / `manual_review` / `rejected` | P0 |
| FR-6.3 | Output confidence score (0.0–1.0) | P0 |
| FR-6.4 | Output human-readable reason string | P0 |
| FR-6.5 | Output list of flags/warnings for manual reviewers | P1 |

### FR-7: Organizer Dashboard
| ID | Requirement | Priority |
|---|---|---|
| FR-7.1 | Display list of all registrations with verification status | P1 |
| FR-7.2 | Filter by status (approved / manual_review / rejected) | P1 |
| FR-7.3 | Show detailed verification breakdown for each registration | P1 |
| FR-7.4 | Allow manual override of decisions | P2 |

---

## 4. Non-Functional Requirements

| ID | Requirement | Target |
|---|---|---|
| NFR-1 | **Latency**: End-to-end verification per registration | < 10 seconds |
| NFR-2 | **False positive rate**: Legitimate participants incorrectly rejected | < 2% |
| NFR-3 | **Accuracy**: Face match true positive rate | > 95% |
| NFR-4 | **Accuracy**: OCR field extraction accuracy | > 90% |
| NFR-5 | **Availability**: System uptime during event registration windows | 99% |
| NFR-6 | **Privacy**: Face embeddings not persisted after verification | Mandatory |
| NFR-7 | **Privacy**: ID images processed in-memory, not stored permanently | Recommended |
| NFR-8 | **Scalability**: Handle concurrent verifications | ≥ 10 simultaneous |
| NFR-9 | **Portability**: Run on commodity hardware (no GPU required for demo) | Mandatory |

---

## 5. User Stories

### Organizer Stories
| ID | Story | Acceptance Criteria |
|---|---|---|
| US-1 | As an organizer, I want uploaded IDs to be automatically verified so I don't have to review each one manually | System processes an uploaded ID and returns a decision within 10 seconds |
| US-2 | As an organizer, I want to see flagged registrations with clear reasons so I can quickly make manual decisions | Dashboard shows flagged registrations with human-readable reasons |
| US-3 | As an organizer, I want to catch participants reusing the same ID under different names | System flags duplicate ID numbers with different registrant names |
| US-4 | As an organizer, I want to set eligibility rules per event (age, student status) | Event config accepts rule parameters; decision engine applies them |

### Participant Stories
| ID | Story | Acceptance Criteria |
|---|---|---|
| US-5 | As a participant, I want to upload my ID and get instant feedback | Upload returns a verification result (not just "processing") |
| US-6 | As a participant, I want clear guidance if my upload fails | Error response includes reason ("Image too blurry") and action ("Please re-upload a clearer photo") |
| US-7 | As a participant, I want my legitimate ID to not be falsely rejected | False positive rate < 2% across test dataset |

---

## 6. Scope

### In Scope (MVP for Hackathon)
- ✅ Image quality & tampering detection
- ✅ Multi-field OCR extraction (name, DOB, ID number, ID type)
- ✅ Face matching (selfie vs. ID photo)
- ✅ Duplicate ID detection
- ✅ Confidence-scored eligibility decisions with reasons
- ✅ Organizer dashboard (basic)
- ✅ REST API for integration
- ✅ Support for Aadhaar, PAN, College ID

### Out of Scope (Post-Hackathon)
- ❌ Production deployment / cloud infrastructure
- ❌ Real-time video liveness detection
- ❌ Integration with DigiLocker / government verification APIs
- ❌ Multi-language UI (English only for demo)
- ❌ Mobile app / native SDK
- ❌ Batch processing of thousands of registrations

---

## 7. Success Metrics

| Metric | Target | How to Measure |
|---|---|---|
| End-to-end verification time | < 10 sec | Timed demo at venue |
| False positive rate | < 2% | Test against sample dataset |
| Fake document detection rate | > 80% | Test with tampered samples |
| Duplicate detection rate | 100% | Test with reused ID numbers |
| Face match accuracy | > 95% | Test with matched/unmatched selfie-ID pairs |
| OCR extraction accuracy | > 90% | Compare extracted fields against ground truth |

---

## 8. Release Plan

| Phase | Timeline | Deliverable |
|---|---|---|
| **Pre-Event Build** | 17 Sept (tonight) | Core pipeline: OCR + face match + duplicate detection + decision engine |
| **Venue Polish** | 18 Sept AM | Dashboard UI, tampering detection, edge-case handling |
| **Demo Ready** | 18 Sept PM | End-to-end working prototype with live demo |
