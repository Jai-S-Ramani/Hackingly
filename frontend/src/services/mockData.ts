import { Registration, JudgePreset } from './types';

export const mockRegistrations: Registration[] = [
  {
    id: "reg-001",
    event_id: "hackathon-2025-ai",
    full_name: "Arjun Sharma",
    id_type: "aadhaar",
    id_number_masked: "XXXX-XXXX-2345",
    dob: "2002-05-14",
    decision: "approved",
    confidence: 0.94,
    reasons: ["UIDAI Verhoeff checksum valid", "ArcFace biometric similarity 94.8%", "Image sharpness variance > 180 (no blur)"],
    created_at: "2026-09-17T20:15:00Z",
    breakdown: {
      quality_passed: true,
      blur_score: 184.2,
      tampering_score: 0.04,
      face_match_score: 0.948,
      face_verdict: "match",
      name_match_score: 0.98,
      is_duplicate: false,
      ocr_extracted: {
        name: "Arjun Sharma",
        dob: "14/05/2002",
        id_number: "453289012345",
        id_type: "aadhaar",
        checksum_valid: true
      }
    }
  },
  {
    id: "reg-002",
    event_id: "hackathon-2025-ai",
    full_name: "Vikram Singh",
    id_type: "aadhaar",
    id_number_masked: "XXXX-XXXX-2345",
    dob: "2003-01-10",
    decision: "rejected",
    confidence: 0.05,
    reasons: ["Duplicate ID Abuse: SHA-256 hash collision with registered participant reg-001 (Arjun Sharma)"],
    created_at: "2026-09-17T20:45:00Z",
    breakdown: {
      quality_passed: true,
      blur_score: 156.4,
      tampering_score: 0.08,
      face_match_score: 0.12,
      face_verdict: "mismatch",
      name_match_score: 0.32,
      is_duplicate: true,
      duplicate_details: "Aadhaar number already registered for Arjun Sharma in this event."
    }
  },
  {
    id: "reg-003",
    event_id: "hackathon-2025-ai",
    full_name: "Priya Raman",
    id_type: "aadhaar",
    id_number_masked: "XXXX-XXXX-7890",
    dob: "2004-11-20",
    decision: "manual_review",
    confidence: 0.71,
    reasons: ["Mild blur detected (Laplacian 88 < 100 threshold)", "Requires human operator visual check of DOB"],
    created_at: "2026-09-17T21:10:00Z",
    breakdown: {
      quality_passed: false,
      blur_score: 88.3,
      tampering_score: 0.12,
      face_match_score: 0.86,
      face_verdict: "match",
      name_match_score: 0.95,
      is_duplicate: false,
      ocr_extracted: {
        name: "Priya Raman",
        dob: "20/11/2004",
        id_number: "987654327890",
        id_type: "aadhaar",
        checksum_valid: true
      }
    }
  },
  {
    id: "reg-004",
    event_id: "hackathon-2025-ai",
    full_name: "Karan Patel",
    id_type: "pan",
    id_number_masked: "ABCDE****F",
    dob: "2001-08-19",
    decision: "approved",
    confidence: 0.91,
    reasons: ["Income Tax Dept PAN format verified", "ArcFace match 91.2%", "Zero ELA compression artifacts"],
    created_at: "2026-09-17T21:30:00Z",
    breakdown: {
      quality_passed: true,
      blur_score: 210.5,
      tampering_score: 0.02,
      face_match_score: 0.912,
      face_verdict: "match",
      name_match_score: 0.96,
      is_duplicate: false,
      ocr_extracted: {
        name: "Karan Patel",
        dob: "19/08/2001",
        id_number: "ABCDE1234F",
        id_type: "pan"
      }
    }
  },
  {
    id: "reg-005",
    event_id: "hackathon-2025-ai",
    full_name: "Sneha Kapoor",
    id_type: "college_id",
    id_number_masked: "2022-CS-****",
    dob: "2003-03-25",
    decision: "approved",
    confidence: 0.88,
    reasons: ["Valid University Roll Number format", "Face similarity 89.5%"],
    created_at: "2026-09-17T21:40:00Z",
    breakdown: {
      quality_passed: true,
      blur_score: 162.0,
      tampering_score: 0.05,
      face_match_score: 0.895,
      face_verdict: "match",
      name_match_score: 0.94,
      is_duplicate: false
    }
  },
  {
    id: "reg-006",
    event_id: "hackathon-2025-ai",
    full_name: "Aditya Verma",
    id_type: "aadhaar",
    id_number_masked: "XXXX-XXXX-9912",
    dob: "2002-12-05",
    decision: "rejected",
    confidence: 0.22,
    reasons: ["High ELA tampering anomaly (0.78) in Date of Birth bounding box", "UIDAI Verhoeff Checksum failed"],
    created_at: "2026-09-17T21:55:00Z",
    breakdown: {
      quality_passed: true,
      blur_score: 145.0,
      tampering_score: 0.78,
      face_match_score: 0.85,
      face_verdict: "match",
      name_match_score: 0.92,
      is_duplicate: false,
      ocr_extracted: {
        name: "Aditya Verma",
        dob: "05/12/2002",
        id_number: "112233449912",
        id_type: "aadhaar",
        checksum_valid: false
      }
    }
  },
  {
    id: "reg-007",
    event_id: "hackathon-2025-ai",
    full_name: "Meera Nair",
    id_type: "college_id",
    id_number_masked: "IITB-22-****",
    dob: "2004-02-14",
    decision: "approved",
    confidence: 0.95,
    reasons: ["Valid Student ID badge", "Face similarity 96.1%"],
    created_at: "2026-09-17T22:05:00Z",
    breakdown: {
      quality_passed: true,
      blur_score: 225.0,
      tampering_score: 0.01,
      face_match_score: 0.961,
      face_verdict: "match",
      name_match_score: 0.99,
      is_duplicate: false
    }
  },
  {
    id: "reg-008",
    event_id: "hackathon-2025-ai",
    full_name: "Rahul Deshmukh",
    id_type: "aadhaar",
    id_number_masked: "XXXX-XXXX-3341",
    dob: "2003-07-22",
    decision: "manual_review",
    confidence: 0.68,
    reasons: ["Glare reflection over photo corner", "Biometric face confidence 72%"],
    created_at: "2026-09-17T22:15:00Z",
    breakdown: {
      quality_passed: false,
      blur_score: 110.0,
      tampering_score: 0.15,
      face_match_score: 0.72,
      face_verdict: "borderline",
      name_match_score: 0.90,
      is_duplicate: false
    }
  },
  {
    id: "reg-009",
    event_id: "hackathon-2025-ai",
    full_name: "Ananya Iyer",
    id_type: "aadhaar",
    id_number_masked: "XXXX-XXXX-8819",
    dob: "2002-09-11",
    decision: "approved",
    confidence: 0.93,
    reasons: ["UIDAI Verhoeff valid", "ArcFace similarity 93.4%"],
    created_at: "2026-09-17T22:25:00Z",
    breakdown: {
      quality_passed: true,
      blur_score: 195.0,
      tampering_score: 0.03,
      face_match_score: 0.934,
      face_verdict: "match",
      name_match_score: 0.97,
      is_duplicate: false
    }
  },
  {
    id: "reg-010",
    event_id: "hackathon-2025-ai",
    full_name: "Impersonator Test",
    id_type: "pan",
    id_number_masked: "FGHIJ****K",
    dob: "2000-04-18",
    decision: "rejected",
    confidence: 0.15,
    reasons: ["Face Mismatch: ID photo and live selfie do not match (ArcFace score 0.18 < 0.65)"],
    created_at: "2026-09-17T22:35:00Z",
    breakdown: {
      quality_passed: true,
      blur_score: 180.0,
      tampering_score: 0.06,
      face_match_score: 0.18,
      face_verdict: "mismatch",
      name_match_score: 0.90,
      is_duplicate: false
    }
  }
];

export const mockJudgePresets: JudgePreset[] = [
  {
    id: "preset-genuine",
    title: "Preset 1: Genuine Aadhaar (Arjun)",
    subtitle: "Clean document, Verhoeff mathematical match, 94.8% ArcFace biometric verification",
    category: "genuine",
    name: "Arjun Sharma",
    idType: "aadhaar",
    idNumber: "453289012345",
    dob: "2002-05-14",
    eventId: "hackathon-2025-ai",
    expectedVerdict: "approved",
    expectedConfidence: 0.94,
    sampleIdPath: "data/samples/sample_aadhaar.png",
    sampleSelfiePath: "data/samples/sample_selfie.png",
    scenarioNotes: "Demonstrates full automatic approval pipeline executing end-to-end in < 900ms."
  },
  {
    id: "preset-duplicate",
    title: "Preset 2: Duplicate ID Abuse (Vikram)",
    subtitle: "Submitting Arjun's Aadhaar under Vikram Singh's name — instant SHA-256 collision",
    category: "duplicate",
    name: "Vikram Singh",
    idType: "aadhaar",
    idNumber: "453289012345",
    dob: "2003-01-10",
    eventId: "hackathon-2025-ai",
    expectedVerdict: "rejected",
    expectedConfidence: 0.05,
    sampleIdPath: "data/samples/sample_duplicate_aadhaar.png",
    sampleSelfiePath: "data/samples/sample_selfie.png",
    scenarioNotes: "Shows zero-knowledge salted hash index blocking multiple team registrations instantly."
  },
  {
    id: "preset-tampered",
    title: "Preset 3: Tampered DOB Photo (Aditya)",
    subtitle: "Digitally altered DOB font detected by Error Level Analysis (ELA) heatmap hotspot",
    category: "tampered",
    name: "Aditya Verma",
    idType: "aadhaar",
    idNumber: "112233449912",
    dob: "2002-12-05",
    eventId: "hackathon-2025-ai",
    expectedVerdict: "rejected",
    expectedConfidence: 0.22,
    sampleIdPath: "data/samples/sample_tampered_aadhaar.png",
    sampleSelfiePath: "data/samples/sample_selfie.png",
    scenarioNotes: "Highlights forensic CV compression artifacts without requiring cloud APIs."
  },
  {
    id: "preset-mismatch",
    title: "Preset 4: Biometric Impersonator",
    subtitle: "Valid ID presented but selfie belongs to a completely different person",
    category: "mismatch",
    name: "Impersonator Test",
    idType: "pan",
    idNumber: "FGHIJ1234K",
    dob: "2000-04-18",
    eventId: "hackathon-2025-ai",
    expectedVerdict: "rejected",
    expectedConfidence: 0.15,
    sampleIdPath: "data/samples/sample_pan.png",
    sampleSelfiePath: "data/samples/sample_mismatch_selfie.png",
    scenarioNotes: "Protects against proxy attendees taking prize money or swag fraudulently."
  }
];
