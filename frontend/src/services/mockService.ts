import { IVerificationService } from './IVerificationService';
import { Registration, TelemetryMetrics, DecisionStatus } from './types';
import { mockRegistrations } from './mockData';

export class MockVerificationService implements IVerificationService {
  private data: Registration[] = [...mockRegistrations];

  async getHealth(): Promise<{ status: string; database: string }> {
    return { status: "healthy", database: "mock_fixtures_active" };
  }

  async getRegistrations(params?: { event_id?: string; status?: string; search?: string }): Promise<Registration[]> {
    let filtered = [...this.data];

    if (params?.status && params.status !== 'all') {
      filtered = filtered.filter(r => r.decision === params.status);
    }

    if (params?.search) {
      const q = params.search.toLowerCase();
      filtered = filtered.filter(r => 
        r.full_name.toLowerCase().includes(q) ||
        r.id_number_masked.toLowerCase().includes(q) ||
        r.id.toLowerCase().includes(q)
      );
    }

    return filtered;
  }

  async getRegistrationById(id: string): Promise<Registration | null> {
    const item = this.data.find(r => r.id === id);
    return item ? { ...item } : null;
  }

  async verifySubmission(formData: FormData): Promise<{
    decision: DecisionStatus;
    confidence: number;
    reasons: string[];
    breakdown: any;
    registration_id: string;
  }> {
    // Simulate real 700ms verification pipeline execution
    await new Promise(res => setTimeout(res, 700));

    const name = (formData.get("name") as string) || "Applicant";
    const idNumber = (formData.get("id_number") as string) || "123456789012";
    const idType = (formData.get("id_type") as any) || "aadhaar";

    // Detect duplicate simulation
    const isDuplicate = this.data.some(r => r.id_number_masked.endsWith(idNumber.slice(-4)) && r.decision === 'approved');

    const decision: DecisionStatus = isDuplicate ? 'rejected' : 'approved';
    const confidence = isDuplicate ? 0.05 : 0.94;
    const reasons = isDuplicate 
      ? [`Duplicate ID Abuse: Hash collision detected for ID ending in ${idNumber.slice(-4)}`]
      : ["UIDAI Verhoeff checksum valid", "ArcFace biometric similarity 94.8%", "Quality passed (no blur)"];

    const newReg: Registration = {
      id: `reg-${Date.now().toString().slice(-4)}`,
      event_id: "hackathon-2025-ai",
      full_name: name,
      id_type: idType,
      id_number_masked: `XXXX-XXXX-${idNumber.slice(-4)}`,
      decision,
      confidence,
      reasons,
      created_at: new Date().toISOString(),
      breakdown: {
        quality_passed: true,
        blur_score: 180.5,
        tampering_score: 0.04,
        face_match_score: 0.948,
        face_verdict: "match",
        name_match_score: 0.98,
        is_duplicate: isDuplicate,
        duplicate_details: isDuplicate ? "ID already registered for another participant" : undefined,
        ocr_extracted: {
          name,
          id_number: idNumber,
          id_type: idType,
          checksum_valid: true
        }
      }
    };

    this.data.unshift(newReg);

    return {
      decision,
      confidence,
      reasons,
      breakdown: newReg.breakdown!,
      registration_id: newReg.id
    };
  }

  async updateReviewDecision(id: string, decision: 'approved' | 'rejected', notes: string): Promise<boolean> {
    const idx = this.data.findIndex(r => r.id === id);
    if (idx >= 0) {
      this.data[idx] = {
        ...this.data[idx],
        decision,
        reasons: [...this.data[idx].reasons, `Manual Review: ${notes}`]
      };
      return true;
    }
    return false;
  }

  async getTelemetry(): Promise<TelemetryMetrics> {
    const total = this.data.length;
    const approved = this.data.filter(r => r.decision === 'approved').length;
    const manual_review = this.data.filter(r => r.decision === 'manual_review').length;
    const rejected = this.data.filter(r => r.decision === 'rejected').length;
    const duplicate_blocked = this.data.filter(r => r.breakdown?.is_duplicate).length;

    const avgConf = total > 0 
      ? this.data.reduce((acc, r) => acc + r.confidence, 0) / total 
      : 0.85;

    return {
      total,
      approved,
      manual_review,
      rejected,
      duplicate_blocked,
      average_confidence: Number(avgConf.toFixed(2)),
      average_latency_ms: 780
    };
  }
}
