'use client';

import React, { useState } from 'react';
import { 
  Camera, 
  CheckCircle2, 
  AlertCircle, 
  User, 
  CreditCard, 
  Calendar,
  FileText
} from 'lucide-react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Badge } from '../ui/Badge';
import { verificationService } from '../../services';
import { useAppStore } from '../../store/useAppStore';

function validateVerhoeff(str: string): boolean {
  const d = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
  ];
  const p = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
  ];
  let c = 0;
  const digits = str.replace(/\D/g, '').split('').map(Number).reverse();
  if (digits.length !== 12) return false;
  for (let i = 0; i < digits.length; i++) {
    c = d[c][p[i % 8][digits[i]]];
  }
  return c === 0;
}

export const ApplicantPortalView: React.FC = () => {
  const { fetchRegistrations, setActiveTab } = useAppStore();
  const [fullName, setFullName] = useState('Ananya Iyer');
  const [idType, setIdType] = useState<'aadhaar' | 'pan' | 'college_id'>('aadhaar');
  const [idNumber, setIdNumber] = useState('453289012345');
  const [dob, setDob] = useState('2003-05-14');
  const [idFile, setIdFile] = useState<File | null>(null);
  const [selfieFile, setSelfieFile] = useState<File | null>(null);
  
  const [isVerhoeffValid, setIsVerhoeffValid] = useState<boolean | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [submissionResult, setSubmissionResult] = useState<any>(null);

  const handleIdNumberBlur = () => {
    if (idType === 'aadhaar') {
      const valid = validateVerhoeff(idNumber);
      setIsVerhoeffValid(valid);
    } else {
      setIsVerhoeffValid(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmissionResult(null);

    const stages = [
      "Checking image quality & blur...",
      "Extracting OCR text & Verhoeff validation...",
      "Matching face biometrics with ArcFace...",
      "Checking duplicate ID abuse index in Supabase...",
      "Synthesizing autonomous decision..."
    ];

    for (let i = 0; i < stages.length; i++) {
      setCurrentStep(i + 1);
      await new Promise(res => setTimeout(res, 200));
    }

    const formData = new FormData();
    formData.append("form_name", fullName);
    formData.append("name", fullName);
    formData.append("form_dob", dob);
    formData.append("dob", dob);
    formData.append("form_email", `${fullName.toLowerCase().replace(/\s+/g, '.')}@example.com`);
    formData.append("event_id", "hackathon-2026");
    formData.append("id_type", idType);
    formData.append("id_number", idNumber);

    if (idFile) {
      formData.append("id_image", idFile);
    } else {
      // Create a fallback placeholder image blob if user didn't pick an explicit file
      const canvas = document.createElement('canvas');
      canvas.width = 400;
      canvas.height = 250;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.fillStyle = '#0F172A';
        ctx.fillRect(0, 0, 400, 250);
        ctx.fillStyle = '#38BDF8';
        ctx.font = '16px monospace';
        ctx.fillText(`ID: ${idNumber}`, 20, 50);
        ctx.fillText(`NAME: ${fullName}`, 20, 90);
        ctx.fillText(`TYPE: ${idType.toUpperCase()}`, 20, 130);
      }
      const blob = await new Promise<Blob>((res) => canvas.toBlob((b) => res(b || new Blob()), 'image/jpeg'));
      formData.append("id_image", new File([blob], `${idType}_document.jpg`, { type: 'image/jpeg' }));
    }

    if (selfieFile) {
      formData.append("selfie", selfieFile);
      formData.append("selfie_image", selfieFile);
    }

    try {
      const result = await verificationService.verifySubmission(formData);
      setSubmissionResult(result);
      await fetchRegistrations();
    } catch (err: any) {
      setSubmissionResult({
        decision: 'rejected',
        confidence: 0.1,
        reasons: [err.message || 'Verification pipeline encountered an error'],
        registration_id: `err-${Date.now().toString().slice(-4)}`
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 space-y-6 select-none animate-in fade-in duration-200">
      {/* Title */}
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          Applicant Identity Verification
        </h2>
        <p className="text-xs text-slate-500 dark:text-slate-400 max-w-lg mx-auto">
          AI Build Challenge Bengaluru · Secure eligibility check with instant autonomous biometric and duplicate detection.
        </p>
      </div>

      {submissionResult ? (
        <Card className="p-6 text-center space-y-5 border-slate-200 dark:border-white/10 shadow-lg dark:shadow-none animate-in zoom-in-95 duration-200">
          <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center mx-auto">
            {submissionResult.decision === 'approved' ? (
              <CheckCircle2 className="w-8 h-8 text-emerald-600 dark:text-emerald-400" />
            ) : submissionResult.decision === 'manual_review' ? (
              <AlertCircle className="w-8 h-8 text-amber-600 dark:text-amber-400" />
            ) : (
              <AlertCircle className="w-8 h-8 text-rose-600 dark:text-rose-400" />
            )}
          </div>

          <div className="space-y-1">
            <Badge status={submissionResult.decision} size="md" />
            <h3 className="text-xl font-bold text-slate-900 dark:text-white mt-2">
              {submissionResult.decision === 'approved' ? 'Identity Verified & Approved!' :
               submissionResult.decision === 'manual_review' ? 'Submission Sent to Manual Review' : 'Verification Rejected'}
            </h3>
            <p className="text-xs text-slate-600 dark:text-slate-400 max-w-md mx-auto leading-relaxed">
              {submissionResult.reasons?.[0] || "Eligibility validated."}
            </p>
          </div>

          <div className="p-3 rounded-xl bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-white/5 max-w-sm mx-auto text-xs font-mono text-slate-600 dark:text-slate-400 flex items-center justify-between">
            <span>REGISTRATION CODE</span>
            <span className="text-indigo-600 dark:text-indigo-400 font-bold">{submissionResult.registration_id}</span>
          </div>

          <div className="flex justify-center gap-3 pt-2">
            <Button variant="secondary" onClick={() => setSubmissionResult(null)}>
              Submit Another ID
            </Button>
            <Button variant="primary" onClick={() => setActiveTab('feed')}>
              View in Live Feed
            </Button>
          </div>
        </Card>
      ) : (
        <Card className="p-6 border-slate-200 dark:border-white/10 shadow-sm dark:shadow-none">
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Full Name Field */}
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                <User className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />
                <span>Full Name (As printed on ID)</span>
              </label>
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950/60 border border-slate-300 dark:border-white/10 rounded-lg text-sm text-slate-900 dark:text-white focus:outline-none focus:border-indigo-500"
              />
            </div>

            {/* ID Type & Number */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                  <CreditCard className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />
                  <span>Document Type</span>
                </label>
                <select
                  value={idType}
                  onChange={(e) => {
                    setIdType(e.target.value as any);
                    setIsVerhoeffValid(null);
                  }}
                  className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-white/10 rounded-lg text-sm text-slate-900 dark:text-white focus:outline-none focus:border-indigo-500"
                >
                  <option value="aadhaar">Aadhaar Card (12 Digits)</option>
                  <option value="pan">PAN Card (10 Chars)</option>
                  <option value="college_id">College / University ID</option>
                </select>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center justify-between">
                  <span>Document / ID Number</span>
                  {idType === 'aadhaar' && isVerhoeffValid !== null && (
                    <span className={`text-[10px] font-mono font-bold ${isVerhoeffValid ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
                      {isVerhoeffValid ? '✓ Verhoeff Valid' : '✗ Checksum Invalid'}
                    </span>
                  )}
                </label>
                <input
                  type="text"
                  required
                  value={idNumber}
                  onChange={(e) => setIdNumber(e.target.value)}
                  onBlur={handleIdNumberBlur}
                  placeholder={idType === 'aadhaar' ? "453289012345" : "ABCDE1234F"}
                  className={`w-full px-3 py-2 bg-slate-50 dark:bg-slate-950/60 border rounded-lg text-sm text-slate-900 dark:text-white font-mono focus:outline-none ${
                    isVerhoeffValid === false ? 'border-rose-500' : 'border-slate-300 dark:border-white/10 focus:border-indigo-500'
                  }`}
                />
              </div>
            </div>

            {/* Date of Birth */}
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                <Calendar className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />
                <span>Date of Birth</span>
              </label>
              <input
                type="date"
                required
                value={dob}
                onChange={(e) => setDob(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950/60 border border-slate-300 dark:border-white/10 rounded-lg text-sm text-slate-900 dark:text-white focus:outline-none focus:border-indigo-500"
              />
            </div>

            {/* Upload Boxes: ID Photo & Selfie */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              {/* ID Document Box */}
              <div 
                onClick={() => document.getElementById('id_upload')?.click()}
                className="p-4 rounded-xl border border-dashed border-slate-300 hover:border-indigo-500 dark:border-white/15 dark:hover:border-indigo-500/50 bg-slate-50/70 hover:bg-slate-100 dark:bg-slate-950/40 dark:hover:bg-slate-950/80 transition-all cursor-pointer text-center space-y-2 group"
              >
                <input
                  type="file"
                  id="id_upload"
                  className="hidden"
                  accept="image/*"
                  onChange={(e) => setIdFile(e.target.files?.[0] || null)}
                />
                <div className="w-9 h-9 rounded-xl bg-slate-200 dark:bg-white/5 flex items-center justify-center mx-auto text-slate-600 dark:text-slate-400 group-hover:text-indigo-600 dark:group-hover:text-indigo-400">
                  <FileText className="w-5 h-5" />
                </div>
                <div>
                  <span className="text-xs font-semibold text-slate-800 dark:text-slate-200 block">
                    {idFile ? idFile.name : "Upload ID Document"}
                  </span>
                  <span className="text-[10px] text-slate-500">Aadhaar, PAN, College ID (PNG, JPG)</span>
                </div>
              </div>

              {/* Live Selfie Box */}
              <div 
                onClick={() => document.getElementById('selfie_upload')?.click()}
                className="p-4 rounded-xl border border-dashed border-slate-300 hover:border-emerald-500 dark:border-white/15 dark:hover:border-emerald-500/50 bg-slate-50/70 hover:bg-slate-100 dark:bg-slate-950/40 dark:hover:bg-slate-950/80 transition-all cursor-pointer text-center space-y-2 group"
              >
                <input
                  type="file"
                  id="selfie_upload"
                  className="hidden"
                  accept="image/*"
                  onChange={(e) => setSelfieFile(e.target.files?.[0] || null)}
                />
                <div className="w-9 h-9 rounded-xl bg-slate-200 dark:bg-white/5 flex items-center justify-center mx-auto text-slate-600 dark:text-slate-400 group-hover:text-emerald-600 dark:group-hover:text-emerald-400">
                  <Camera className="w-5 h-5" />
                </div>
                <div>
                  <span className="text-xs font-semibold text-slate-800 dark:text-slate-200 block">
                    {selfieFile ? selfieFile.name : "Upload / Capture Selfie"}
                  </span>
                  <span className="text-[10px] text-slate-500">Live facial photo for biometric match</span>
                </div>
              </div>
            </div>

            {/* Stepper Progress Bar */}
            {isSubmitting && (
              <div className="p-3 rounded-xl bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-white/10 space-y-2 animate-in fade-in">
                <div className="flex items-center justify-between text-xs text-indigo-600 dark:text-indigo-400 font-semibold">
                  <span>Executing Pipeline Step {currentStep} of 5</span>
                  <span className="font-mono">{currentStep * 20}%</span>
                </div>
                <div className="w-full bg-slate-200 dark:bg-white/5 rounded-full h-1.5 overflow-hidden">
                  <div 
                    className="bg-gradient-to-r from-indigo-500 to-emerald-400 h-full transition-all duration-200"
                    style={{ width: `${currentStep * 20}%` }}
                  />
                </div>
              </div>
            )}

            {/* Submit Button */}
            <Button
              variant="primary"
              size="lg"
              fullWidth
              type="submit"
              isLoading={isSubmitting}
            >
              Verify Eligibility & Register
            </Button>
          </form>
        </Card>
      )}
    </div>
  );
};
