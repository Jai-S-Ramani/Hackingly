'use client';

import React from 'react';
import { 
  ShieldCheck, 
  Sparkles, 
  ArrowRight, 
  Camera, 
  Activity, 
  AlertTriangle, 
  CheckCircle2, 
  Clock, 
  FileSearch,
  ExternalLink
} from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { mockJudgePresets } from '../../services/mockData';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { VerispectLogo } from '../brand/VerispectLogo';

export const HeroHubView: React.FC = () => {
  const { 
    setActiveTab, 
    setActivePreset, 
    registrations, 
    telemetry,
    setSelectedRegistration 
  } = useAppStore();

  const total = telemetry?.total ?? registrations.length ?? 0;
  const approved = telemetry?.approved ?? registrations.filter(r => r.decision === 'approved').length ?? 0;
  const reviews = telemetry?.manual_review ?? registrations.filter(r => r.decision === 'manual_review').length ?? 0;
  const rejected = telemetry?.rejected ?? registrations.filter(r => r.decision === 'rejected').length ?? 0;
  const blocked = telemetry?.duplicate_blocked ?? registrations.filter(r => r.breakdown?.is_duplicate || r.decision === 'rejected').length ?? 0;
  const avgConfidence = telemetry?.average_confidence ? Math.round(telemetry.average_confidence * 100) : 92;
  const latency = telemetry?.average_latency_ms ?? 680;

  const approvalRate = total > 0 ? Math.round((approved / total) * 100) : 85;

  const handlePresetSelect = (preset: any) => {
    setActivePreset(preset);
    setActiveTab('sandbox');
  };

  const recentRegistrations = registrations.slice(0, 4);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-6 sm:py-8 space-y-8 animate-in fade-in duration-300">
      {/* Brand Hero Header */}
      <div className="text-center space-y-4 max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-medium border border-indigo-500/25 bg-indigo-500/10 text-indigo-700 dark:text-indigo-300 backdrop-blur-md">
          <Sparkles className="w-3.5 h-3.5 text-indigo-500 dark:text-indigo-400" />
          <span className="font-mono">Verispect Core v1.2 — Biometric & Cryptographic ID Intelligence</span>
        </div>

        <div className="flex justify-center py-1">
          <VerispectLogo variant="symbol" size={56} animated={true} status="default" />
        </div>

        <h1 className="text-3xl sm:text-5xl font-extrabold text-slate-900 dark:text-white tracking-tight leading-tight">
          Forensic Precision. <br className="hidden sm:inline" />
          <span className="bg-gradient-to-r from-indigo-600 via-cyan-600 to-emerald-600 dark:from-indigo-400 dark:via-cyan-300 dark:to-emerald-400 bg-clip-text text-transparent">
            Uncompromising Trust.
          </span>
        </h1>

        <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 leading-relaxed">
          Automated multi-spectral document forensics: UIDAI Verhoeff checksum validation, 
          Laplacian blur & ELA tamper analysis, ArcFace facial biometric verification, and zero-knowledge 
          SHA-256 duplicate collision detection.
        </p>

        {/* Primary Action Row */}
        <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
          <button
            onClick={() => setActiveTab('portal')}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm transition-all shadow-lg shadow-indigo-600/25 border border-indigo-500/30 cursor-pointer active:scale-[0.98]"
          >
            <Camera className="w-4 h-4" />
            <span>Launch Applicant Verification</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            onClick={() => setActiveTab('feed')}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 dark:bg-white/5 dark:hover:bg-white/10 dark:text-slate-200 dark:hover:text-white font-semibold text-sm border border-slate-200 dark:border-white/10 transition-all cursor-pointer"
          >
            <FileSearch className="w-4 h-4 text-indigo-500" />
            <span>View Live Audit Feed</span>
          </button>
        </div>
      </div>

      {/* Live Operational Metrics Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        {/* Metric 1: Total Verified */}
        <Card className="p-4 sm:p-5 border-slate-200 dark:border-white/10">
          <div className="flex items-center justify-between text-slate-500 dark:text-slate-400 mb-2">
            <span className="text-xs font-bold font-mono uppercase">Total Processed</span>
            <Activity className="w-4 h-4 text-indigo-500" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white font-mono">
            {total}
          </div>
          <p className="text-[11px] text-slate-500 mt-1 flex items-center gap-1">
            <span className="text-emerald-600 dark:text-emerald-400 font-bold">{approvalRate}%</span> auto-approved
          </p>
        </Card>

        {/* Metric 2: Manual Review Queue */}
        <Card className="p-4 sm:p-5 border-slate-200 dark:border-white/10">
          <div className="flex items-center justify-between text-slate-500 dark:text-slate-400 mb-2">
            <span className="text-xs font-bold font-mono uppercase">Pending Review</span>
            <AlertTriangle className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-amber-600 dark:text-amber-400 font-mono">
            {reviews}
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Requires human operator</p>
        </Card>

        {/* Metric 3: Fraud & Collisions Blocked */}
        <Card className="p-4 sm:p-5 border-slate-200 dark:border-white/10">
          <div className="flex items-center justify-between text-slate-500 dark:text-slate-400 mb-2">
            <span className="text-xs font-bold font-mono uppercase">Fraud Intercepted</span>
            <CheckCircle2 className="w-4 h-4 text-rose-500" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-rose-600 dark:text-rose-400 font-mono">
            {blocked}
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Duplicate & tamper blocks</p>
        </Card>

        {/* Metric 4: Average Pipeline Latency */}
        <Card className="p-4 sm:p-5 border-slate-200 dark:border-white/10">
          <div className="flex items-center justify-between text-slate-500 dark:text-slate-400 mb-2">
            <span className="text-xs font-bold font-mono uppercase">Pipeline Latency</span>
            <Clock className="w-4 h-4 text-cyan-500" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-cyan-600 dark:text-cyan-400 font-mono">
            {latency}ms
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Sub-second decision engine</p>
        </Card>
      </div>

      {/* Two Column Section: Recent Verifications & Judge Scenarios */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Recent Audit Log (8 cols) */}
        <div className="lg:col-span-7 space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-slate-900 dark:text-white uppercase font-mono tracking-wider">
              Recent Verification Audits
            </h2>
            <button
              onClick={() => setActiveTab('feed')}
              className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1 cursor-pointer"
            >
              <span>Explore All</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <Card className="divide-y divide-slate-200 dark:divide-white/8 border-slate-200 dark:border-white/10 overflow-hidden">
            {recentRegistrations.map((r) => (
              <div
                key={r.id}
                onClick={() => setSelectedRegistration(r)}
                className="p-3.5 sm:p-4 flex items-center justify-between hover:bg-slate-50 dark:hover:bg-white/[0.03] transition-colors cursor-pointer group"
              >
                <div className="flex items-center gap-3 min-w-0">
                  <div className="w-9 h-9 rounded-xl bg-slate-100 dark:bg-white/5 border border-slate-200 dark:border-white/10 flex items-center justify-center text-xs font-mono font-bold text-slate-700 dark:text-slate-300 shrink-0">
                    {(r.id_type || 'ID').slice(0, 3).toUpperCase()}
                  </div>
                  <div className="min-w-0">
                    <div className="text-sm font-bold text-slate-900 dark:text-white truncate group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                      {r.full_name}
                    </div>
                    <div className="text-xs text-slate-500 font-mono truncate">
                      {r.id_number_masked} · <span className="opacity-80">{r.id}</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2 sm:gap-3 shrink-0">
                  <Badge decision={r.decision} />
                  <span className="text-xs font-mono font-bold text-slate-700 dark:text-slate-300 hidden sm:inline">
                    {Math.round(r.confidence * 100)}%
                  </span>
                  <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-indigo-500 transition-colors" />
                </div>
              </div>
            ))}
          </Card>
        </div>

        {/* Right Column: Quick Judge Presets (5 cols) */}
        <div className="lg:col-span-5 space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-slate-900 dark:text-white uppercase font-mono tracking-wider">
              Judge 1-Click Test Scenarios
            </h2>
            <Sparkles className="w-3.5 h-3.5 text-indigo-500" />
          </div>

          <div className="space-y-2.5">
            {mockJudgePresets.slice(0, 3).map((p) => (
              <Card
                key={p.id}
                hoverable
                onClick={() => handlePresetSelect(p)}
                className="p-3.5 border-slate-200 dark:border-white/10 hover:border-indigo-500/40 group cursor-pointer"
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/20 uppercase">
                      {p.category}
                    </span>
                    <h4 className="text-xs sm:text-sm font-bold text-slate-900 dark:text-white mt-1.5 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                      {p.title}
                    </h4>
                    <p className="text-xs text-slate-500 mt-1 line-clamp-2 leading-relaxed">
                      {p.subtitle}
                    </p>
                  </div>
                  <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-indigo-500 group-hover:translate-x-0.5 transition-all shrink-0 mt-1" />
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
export default HeroHubView;
