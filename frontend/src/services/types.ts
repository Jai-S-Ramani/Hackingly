export type DecisionStatus = 'approved' | 'manual_review' | 'rejected';

export type IdType = 'aadhaar' | 'pan' | 'college_id' | 'passport';

export interface VerificationBreakdown {
  quality_passed?: boolean;
  blur_score?: number;
  tampering_score?: number;
  ela_heatmap_url?: string;
  ocr_extracted?: {
    name?: string;
    dob?: string;
    id_number?: string;
    id_type?: string;
    checksum_valid?: boolean;
  };
  face_match_score?: number;
  face_verdict?: string;
  name_match_score?: number;
  is_duplicate?: boolean;
  duplicate_details?: string;
  reasons?: string[];
}

export interface Registration {
  id: string;
  event_id: string;
  full_name: string;
  id_type: IdType;
  id_number_masked: string;
  dob?: string;
  decision: DecisionStatus;
  confidence: number;
  reasons: string[];
  created_at: string;
  id_image_url?: string;
  selfie_image_url?: string;
  breakdown?: VerificationBreakdown;
}

export interface TelemetryMetrics {
  total: number;
  approved: number;
  manual_review: number;
  rejected: number;
  duplicate_blocked: number;
  average_confidence: number;
  average_latency_ms: number;
}

export interface JudgePreset {
  id: string;
  title: string;
  subtitle: string;
  category: 'genuine' | 'duplicate' | 'tampered' | 'mismatch';
  name: string;
  idType: IdType;
  idNumber: string;
  dob: string;
  eventId: string;
  expectedVerdict: DecisionStatus;
  expectedConfidence: number;
  sampleIdPath: string;
  sampleSelfiePath: string;
  scenarioNotes: string;
}
