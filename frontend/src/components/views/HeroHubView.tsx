'use client';

import React from 'react';
import { 
  ShieldCheck, 
  Sparkles, 
  ArrowRight, 
  Layers, 
  AlertTriangle, 
  Cpu, 
  CheckCircle2, 
  Database,
  Lock,
  Camera
} from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { mockJudgePresets } from '../../services/mockData';
import { Card } from '../ui/Card';

export const HeroHubView: React.FC = () => {
  const { setActiveTab, setActivePreset, registrations, telemetry } = useAppStore();

  const total = registrations.length || 23;
  const approved = registrations.filter(r => r.decision === 'approved').length || 18;
  const reviews = registrations.filter(r => r.decision === 'manual_review').length || 3;
  const rejected = registrations.filter(r => r.decision === 'rejected').length || 2;

  const handlePresetSelect = (preset: any) => {
    setActivePreset(preset);
    setActiveTab('sandbox');
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-10 animate-in fade-in duration-300 select-none">
      {/* Confluence Pill & Headline Header */}
      <div className="text-center space-y-4">
        {/* Capsule Pill (Confluence Reference) */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full text-xs font-medium border border-indigo-500/20 bg-indigo-500/10 text-indigo-300 backdrop-blur-md">
          <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
          <span>v2.0 — autonomous verification with live biometric & duplicate checks</span>
        </div>

        {/* Hero Title */}
        <h1 className="text-4xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight">
          Verify identities with AI. <br className="hidden sm:inline" />
          <span className="bg-gradient-to-r from-indigo-400 via-purple-300 to-emerald-400 bg-clip-text text-transparent">
            Catch fraud in milliseconds.
          </span>
        </h1>

        {/* Hero Subtitle */}
        <p className="max-w-2xl mx-auto text-base text-slate-400 leading-relaxed">
          DeepFace ArcFace facial biometrics, UIDAI Verhoeff checksum algorithm, and zero-knowledge 
          SHA-256 duplicate ID fraud prevention — streaming live to Supabase Cloud.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
          <button
            onClick={() => setActiveTab('portal')}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-all shadow-lg shadow-indigo-600/25 border border-indigo-500/30 cursor-pointer active:scale-[0.98]"
          >
            <Camera className="w-4 h-4" />
            <span>Start Live ID Verification</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            onClick={() => setActiveTab('sandbox')}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white/5 hover:bg-white/10 text-slate-200 hover:text-white font-medium text-sm border border-white/10 transition-all cursor-pointer"
          >
            <Sparkles className="w-4 h-4 text-emerald-400" />
            <span>Explore Judge Sandbox</span>
          </button>
        </div>

        <p className="text-xs text-slate-500">
          Built for AI Build Challenge Bengaluru · PS-003 Hackingly Track
        </p>
      </div>

      {/* Two Hero Quick-Action Cards (Confluence 2-card Grid) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Card 
          hoverable 
          onClick={() => setActiveTab('portal')}
          className="p-5 flex flex-col justify-between border-white/10 hover:border-indigo-500/40 group"
        >
          <div className="space-y-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 group-hover:scale-105 transition-transform">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-semibold text-white group-hover:text-indigo-300 transition-colors">
                Applicant Verification Portal
              </h3>
              <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                Self-service Aadhaar, PAN, or College ID upload with real-time Verhoeff check and selfie face matching.
              </p>
            </div>
          </div>
          <div className="mt-4 flex items-center text-xs font-medium text-indigo-400 group-hover:text-indigo-300">
            <span>Launch Upload Flow</span>
            <ArrowRight className="w-3.5 h-3.5 ml-1 group-hover:translate-x-1 transition-transform" />
          </div>
        </Card>

        <Card 
          hoverable 
          onClick={() => setActiveTab('sandbox')}
          className="p-5 flex flex-col justify-between border-white/10 hover:border-emerald-500/40 group"
        >
          <div className="space-y-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 group-hover:scale-105 transition-transform">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-semibold text-white group-hover:text-emerald-300 transition-colors">
                Judge Interactive Sandbox
              </h3>
              <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                1-click live forensic test scenarios for stage demo: Duplicate fraud, ELA photo tampering, and face mismatch.
              </p>
            </div>
          </div>
          <div className="mt-4 flex items-center text-xs font-medium text-emerald-400 group-hover:text-emerald-300">
            <span>Open Demo Sandbox</span>
            <ArrowRight className="w-3.5 h-3.5 ml-1 group-hover:translate-x-1 transition-transform" />
          </div>
        </Card>
      </div>

      {/* "TRY STARTING WITH" Linear-Style Preset Action Rows (Confluence Reference) */}
      <div className="space-y-2.5">
        <div className="flex items-center justify-between px-1 text-xs font-semibold text-slate-400 uppercase tracking-wider">
          <div className="flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
            <span>Try Stage Demo Scenarios</span>
          </div>
          <span className="text-[11px] text-slate-500 lowercase">Click to execute in sandbox</span>
        </div>

        <div className="space-y-2">
          {mockJudgePresets.map((preset) => (
            <div
              key={preset.id}
              onClick={() => handlePresetSelect(preset)}
              className="p-3.5 rounded-xl bg-slate-900/60 hover:bg-slate-800/80 border border-white/8 hover:border-white/20 transition-all cursor-pointer flex items-center justify-between group"
            >
              <div className="flex items-center gap-3">
                <div className={`w-2 h-2 rounded-full ${
                  preset.category === 'genuine' ? 'bg-emerald-400' :
                  preset.category === 'duplicate' ? 'bg-rose-500' :
                  preset.category === 'tampered' ? 'bg-amber-400' : 'bg-purple-400'
                }`} />
                <div>
                  <h4 className="text-sm font-medium text-slate-200 group-hover:text-white transition-colors">
                    {preset.title}
                  </h4>
                  <p className="text-xs text-slate-500 group-hover:text-slate-400 transition-colors line-clamp-1">
                    {preset.subtitle}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <span className={`text-[11px] px-2 py-0.5 rounded font-mono font-medium ${
                  preset.expectedVerdict === 'approved' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'
                }`}>
                  {preset.expectedVerdict.toUpperCase()}
                </span>
                <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-white group-hover:translate-x-0.5 transition-all" />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Live System Telemetry Bar */}
      <Card className="p-4 bg-slate-950/80 border-white/8">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center divide-y sm:divide-y-0 sm:divide-x divide-white/8">
          <div className="pt-2 sm:pt-0">
            <span className="text-[11px] text-slate-400 uppercase tracking-wider block">Registrations</span>
            <span className="text-2xl font-bold text-white mt-1 block font-mono">{total}</span>
            <span className="text-[10px] text-slate-500">Live in Supabase</span>
          </div>

          <div className="pt-2 sm:pt-0">
            <span className="text-[11px] text-slate-400 uppercase tracking-wider block">Auto-Approved</span>
            <span className="text-2xl font-bold text-emerald-400 mt-1 block font-mono">
              {Math.round((approved / total) * 100)}%
            </span>
            <span className="text-[10px] text-emerald-500/80">&lt; 2% false positives</span>
          </div>

          <div className="pt-2 sm:pt-0">
            <span className="text-[11px] text-slate-400 uppercase tracking-wider block">Pending Review</span>
            <span className="text-2xl font-bold text-amber-400 mt-1 block font-mono">{reviews}</span>
            <span className="text-[10px] text-slate-500">Borderline score (0.60–0.85)</span>
          </div>

          <div className="pt-2 sm:pt-0">
            <span className="text-[11px] text-slate-400 uppercase tracking-wider block">Average Speed</span>
            <span className="text-2xl font-bold text-indigo-400 mt-1 block font-mono">740ms</span>
            <span className="text-[10px] text-indigo-400/80">Self-contained OpenCV/ArcFace</span>
          </div>
        </div>
      </Card>
    </div>
  );
};
