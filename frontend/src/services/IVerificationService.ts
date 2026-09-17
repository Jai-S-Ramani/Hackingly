import { Registration, TelemetryMetrics, VerificationBreakdown, DecisionStatus } from './types';

export interface IVerificationService {
  getHealth(): Promise<{ status: string; database: string }>;
  getRegistrations(params?: { event_id?: string; status?: string; search?: string }): Promise<Registration[]>;
  getRegistrationById(id: string): Promise<Registration | null>;
  verifySubmission(formData: FormData): Promise<{
    decision: DecisionStatus;
    confidence: number;
    reasons: string[];
    breakdown: VerificationBreakdown;
    registration_id: string;
  }>;
  updateReviewDecision(id: string, decision: 'approved' | 'rejected', notes: string): Promise<boolean>;
  getTelemetry(): Promise<TelemetryMetrics>;
}
