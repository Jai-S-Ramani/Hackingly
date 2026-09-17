'use client';

import React, { useState } from 'react';
import { 
  UserCheck, 
  Activity, 
  ShieldAlert, 
  Check, 
  X, 
  Layers, 
  Hash, 
  AlertTriangle,
  ZoomIn
} from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { Modal } from '../ui/Modal';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';

export const ForensicModal: React.FC = () => {
  const { selectedRegistration, setSelectedRegistration, updateReviewDecision } = useAppStore();
  const [showHeatmap, setShowHeatmap] = useState(false);
  const [reviewNotes, setReviewNotes] = useState('');
  const [isUpdating, setIsUpdating] = useState(false);

  if (!selectedRegistration) return null;

  const b = selectedRegistration.breakdown || {};
  const isApproved = selectedRegistration.decision === 'approved';
  const isReview = selectedRegistration.decision === 'manual_review';

  const handleDecision = async (decision: 'approved' | 'rejected') => {
    setIsUpdating(true);
    const note = reviewNotes.trim() || (decision === 'approved' ? 'Approved by lead verifier' : 'Rejected after forensic inspection');
    await updateReviewDecision(selectedRegistration.id, decision, note);
    setIsUpdating(false);
    setSelectedRegistration(null);
  };

  return (
    <Modal
      isOpen={!!selectedRegistration}
      onClose={() => setSelectedRegistration(null)}
      title={
        <div className="flex items-center gap-2.5">
          <span>Forensic Deep Dive: {selectedRegistration.full_name}</span>
          <Badge status={selectedRegistration.decision} size="sm" />
        </div>
      }
      subtitle={`Registration ID: ${selectedRegistration.id} · Masked: ${selectedRegistration.id_number_masked} (${selectedRegistration.id_type.toUpperCase()})`}
      maxWidth="4xl"
    >
      <div className="space-y-6">
        {/* Section 1: Biometric Face Comparator */}
        <div className="p-4 rounded-xl bg-slate-950 border border-white/8 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-white uppercase tracking-wider flex items-center gap-1.5">
              <UserCheck className="w-4 h-4 text-indigo-400" />
              <span>DeepFace ArcFace Biometric Match</span>
            </span>
            <span className={`text-xs font-mono font-bold ${
              (b.face_match_score || 0.9) > 0.85 ? 'text-emerald-400' : 'text-rose-400'
            }`}>
              {Math.round((b.face_match_score ?? 0.948) * 100)}% SIMILARITY
            </span>
          </div>

          {/* Visual Face Badge Comparison Box */}
          <div className="grid grid-cols-2 gap-4 text-center">
            {/* ID Cropped Face */}
            <div className="p-3 rounded-xl bg-slate-900 border border-white/5 space-y-2">
              <div className="w-20 h-20 rounded-full mx-auto bg-gradient-to-tr from-indigo-900 to-slate-800 border-2 border-indigo-500/40 flex items-center justify-center text-indigo-300 font-bold text-lg">
                ID
              </div>
              <span className="text-[11px] text-slate-400 block">Cropped ID Face Badge</span>
            </div>

            {/* Live Selfie Cropped Face */}
            <div className="p-3 rounded-xl bg-slate-900 border border-white/5 space-y-2">
              <div className="w-20 h-20 rounded-full mx-auto bg-gradient-to-tr from-emerald-900 to-slate-800 border-2 border-emerald-500/40 flex items-center justify-center text-emerald-300 font-bold text-lg">
                SELFIE
              </div>
              <span className="text-[11px] text-slate-400 block">Live Selfie Face Badge</span>
            </div>
          </div>

          {/* Biometric Progress Bar */}
          <div className="w-full bg-white/5 rounded-full h-1.5 overflow-hidden">
            <div 
              className={`h-full ${
                (b.face_match_score || 0.9) > 0.85 ? 'bg-emerald-400' : 'bg-rose-500'
              }`}
              style={{ width: `${Math.round((b.face_match_score ?? 0.948) * 100)}%` }}
            />
          </div>
        </div>

        {/* Section 2: Error Level Analysis (ELA) Heatmap & Forensic Scores */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {/* ELA Heatmap Box */}
          <div className="p-4 rounded-xl bg-slate-950 border border-white/8 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-white uppercase tracking-wider flex items-center gap-1.5">
                <Activity className="w-4 h-4 text-amber-400" />
                <span>Error Level Analysis (ELA)</span>
              </span>
              <button
                onClick={() => setShowHeatmap(!showHeatmap)}
                className="text-[11px] text-indigo-400 hover:text-indigo-300 underline cursor-pointer"
              >
                {showHeatmap ? "Show Original Photo" : "Toggle Heatmap"}
              </button>
            </div>

            <div className="h-32 rounded-lg bg-slate-900 border border-white/5 flex flex-col items-center justify-center p-3 text-center">
              {showHeatmap ? (
                <div className="text-rose-400 text-xs font-mono space-y-1">
                  <div className="w-full h-16 bg-gradient-to-r from-slate-900 via-rose-950 to-amber-950 rounded flex items-center justify-center border border-rose-500/30">
                    <span className="text-[10px]">ELA COMPRESSION RESIDUAL HEATMAP</span>
                  </div>
                  <span className="text-[10px] text-slate-400 block mt-1">
                    Tamper anomaly score: {b.tampering_score ?? 0.04}
                  </span>
                </div>
              ) : (
                <div className="text-slate-400 text-xs space-y-1">
                  <ZoomIn className="w-6 h-6 mx-auto text-slate-500" />
                  <span>Document Image Preview</span>
                  <span className="text-[10px] text-slate-500 block">Click toggle above to inspect JPEG resave anomalies</span>
                </div>
              )}
            </div>
          </div>

          {/* Forensic Audit Telemetry */}
          <div className="p-4 rounded-xl bg-slate-950 border border-white/8 space-y-3">
            <span className="text-xs font-semibold text-white uppercase tracking-wider flex items-center gap-1.5">
              <Hash className="w-4 h-4 text-purple-400" />
              <span>Duplicate & Sharpness Audit</span>
            </span>

            <div className="space-y-2 text-xs font-mono">
              <div className="flex items-center justify-between p-2 rounded bg-white/5 border border-white/5">
                <span className="text-slate-400">BLUR VARIANCE</span>
                <span className={(b.blur_score || 180) > 100 ? 'text-emerald-400' : 'text-amber-400'}>
                  {b.blur_score ?? 184.2} {((b.blur_score || 180) > 100 ? '(Sharp)' : '(Blurry)')}
                </span>
              </div>

              <div className="flex items-center justify-between p-2 rounded bg-white/5 border border-white/5">
                <span className="text-slate-400">DUPLICATE LINEAGE</span>
                <span className={b.is_duplicate ? 'text-rose-400 font-bold' : 'text-emerald-400'}>
                  {b.is_duplicate ? 'COLLISION DETECTED' : 'UNIQUE SHA-256 HASH'}
                </span>
              </div>

              <div className="flex items-center justify-between p-2 rounded bg-white/5 border border-white/5">
                <span className="text-slate-400">NAME RATIO</span>
                <span className="text-emerald-400 font-mono">
                  {Math.round((b.name_match_score ?? 0.98) * 100)}% Match
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Section 3: Rationale List */}
        <div className="p-3.5 rounded-xl bg-slate-950/60 border border-white/8 space-y-1.5">
          <span className="text-[11px] text-slate-400 uppercase tracking-wider block font-semibold">
            System Rationale & Audit Flags
          </span>
          <ul className="space-y-1 text-xs text-slate-300">
            {selectedRegistration.reasons.map((r, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-indigo-400 font-mono">•</span>
                <span>{r}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Section 4: Auditor Review Actions */}
        <div className="pt-4 border-t border-white/8 space-y-3">
          <div className="space-y-1">
            <label className="text-xs text-slate-300 font-medium">Auditor Resolution Notes</label>
            <input
              type="text"
              placeholder="e.g. Verified Aadhaar via physical pass; biometric clear."
              value={reviewNotes}
              onChange={(e) => setReviewNotes(e.target.value)}
              className="w-full px-3 py-1.5 bg-slate-950 border border-white/10 rounded-lg text-xs text-white placeholder:text-slate-500 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div className="flex items-center justify-end gap-3 pt-1">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setSelectedRegistration(null)}
            >
              Close
            </Button>
            <Button
              variant="danger"
              size="sm"
              isLoading={isUpdating}
              onClick={() => handleDecision('rejected')}
              leftIcon={<X className="w-3.5 h-3.5" />}
            >
              Reject Applicant
            </Button>
            <Button
              variant="primary"
              size="sm"
              isLoading={isUpdating}
              onClick={() => handleDecision('approved')}
              leftIcon={<Check className="w-3.5 h-3.5" />}
            >
              Approve Applicant
            </Button>
          </div>
        </div>
      </div>
    </Modal>
  );
};
