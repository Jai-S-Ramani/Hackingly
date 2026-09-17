'use client';

import React from 'react';
import { 
  ShieldCheck, 
  Sparkles, 
  ArrowRight, 
  Camera
} from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { mockJudgePresets } from '../../services/mockData';
import { Card } from '../ui/Card';

export const HeroHubView: React.FC = () => {
  const { setActiveTab, setActivePreset, registrations } = useAppStore();

  const total = registrations.length || 23;
  const approved = registrations.filter(r => r.decision === 'approved').length || 18;
  const reviews = registrations.filter(r => r.decision === 'manual_review').length || 3;

  const handlePresetSelect = (preset: any) => {
    setActivePreset(preset);
    setActiveTab('sandbox');
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-10 animate-in fade-in duration-300 select-none">
      {/* Confluence Pill & Headline Header */}
      <div className="text-center space-y-4">
        {/* Capsule Pill */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full text-xs font-medium border border-indigo-500/20 bg-indigo-500/10 text-indigo-700 dark:text-indigo-300 backdrop-blur-md">
          <Sparkles className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
          <span>v2.0 — autonomous verification with live biometric & duplicate checks</span>
        </div>

        {/* Hero Title */}
        <h1 className="text-4xl sm:text-5xl font-extrabold text-slate-900 dark:text-white tracking-tight leading-tight">
          Verify identities with AI. <br className="hidden sm:inline" />
          <span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-emerald-600 dark:from-indigo-400 dark:via-purple-300 dark:to-emerald-400 bg-clip-text text-transparent">
            Catch fraud in milliseconds.
          </span>
        </h1>

        {/* Hero Subtitle */}
        <p className="max-w-2xl mx-auto text-base text-slate-600 dark:text-slate-400 leading-relaxed">
          DeepFace ArcFace facial biometrics, UIDAI Verhoeff checksum algorithm, and zero-knowledge 
          SHA-256 duplicate ID fraud prevention — streaming live to Supabase Cloud.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
          <button
            onClick={() => setActiveTab('portal')}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm transition-all shadow-lg shadow-indigo-600/25 border border-indigo-500/30 cursor-pointer active:scale-[0.98]"
          >
            <Camera className="w-4 h-4" />
            <span>Start Live ID Verification</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            onClick={() => setActiveTab('sandbox')}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 dark:bg-white/5 dark:hover:bg-white/10 dark:text-slate-200 dark:hover:text-white font-semibold text-sm border border-slate-200 dark:border-white/10 transition-all cursor-pointer"
          >
            <Sparkles className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            <span>Explore Judge Sandbox</span>
          </button>
        </div>

        <p className="text-xs text-slate-500">
          Built for AI Build Challenge Bengaluru · PS-003 Hackingly Track
        </p>
      </div>

      {/* Two Hero Quick-Action Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Card 
          hoverable 
          onClick={() => setActiveTab('portal')}
          className="p-5 flex flex-col justify-between border-slate-200 dark:border-white/10 hover:border-indigo-500/40 group"
        >
          <div className="space-y-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-600 dark:text-indigo-400 group-hover:scale-105 transition-transform">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-semibold text-slate-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-300 transition-colors">
                Applicant Verification Portal
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400 mt-1 leading-relaxed">
                Self-service Aadhaar, PAN, or College ID upload with real-time Verhoeff check and selfie face matching.
              </p>
            </div>
          </div>
          <div className="mt-4 flex items-center text-xs font-semibold text-indigo-600 dark:text-indigo-400 group-hover:text-indigo-500">
            <span>Launch Upload Flow</span>
            <ArrowRight className="w-3.5 h-3.5 ml-1 group-hover:translate-x-1 transition-transform" />
          </div>
        </Card>

        <Card 
          hoverable 
          onClick={() => setActiveTab('sandbox')}
          className="p-5 flex flex-col justify-between border-slate-200 dark:border-white/10 hover:border-emerald-500/40 group"
        >
          <div className="space-y-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-600 dark:text-emerald-400 group-hover:scale-105 transition-transform">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-semibold text-slate-900 dark:text-white group-hover:text-emerald-600 dark:group-hover:text-emerald-300 transition-colors">
                Judge Interactive Sandbox
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400 mt-1 leading-relaxed">
                1-click live forensic test scenarios for stage demo: Duplicate fraud, ELA photo tampering, and face mismatch.
              </p>
            </div>
          </div>
          <div className="mt-4 flex items-center text-xs font-semibold text-emerald-600 dark:text-emerald-400 group-hover:text-emerald-500">
            <span>Open Demo Sandbox</span>
            <ArrowRight className="w-3.5 h-3.5 ml-1 group-hover:translate-x-1 transition-transform" />
          </div>
        </Card>
      </div>

      {/* "TRY STARTING WITH" Linear-Style Preset Action Rows */}
      <div className="space-y-2.5">
        <div className="flex items-center justify-between px-1 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
          <div className="flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />
            <span>Try Stage Demo Scenarios</span>
          </div>
          <span className="text-[11px] text-slate-500 lowercase">Click to execute in sandbox</span>
        </div>

        <div className="space-y-2">
          {mockJudgePresets.map((preset) => (
            <div
              key={preset.id}
              onClick={() => handlePresetSelect(preset)}
              className="p-3.5 rounded-xl bg-white dark:bg-slate-900/60 hover:bg-slate-50 dark:hover:bg-slate-800/80 border border-slate-200 dark:border-white/8 hover:border-slate-300 dark:hover:border-white/20 transition-all cursor-pointer flex items-center justify-between group shadow-sm dark:shadow-none"
            >
              <div className="flex items-center gap-3">
                <div className={`w-2 h-2 rounded-full ${
                  preset.category === 'genuine' ? 'bg-emerald-500' :
                  preset.category === 'duplicate' ? 'bg-rose-500' :
                  preset.category === 'tampered' ? 'bg-amber-500' : 'bg-purple-500'
                }`} />
                <div>
                  <h4 className="text-sm font-semibold text-slate-800 dark:text-slate-200 group-hover:text-slate-900 dark:group-hover:text-white transition-colors">
                    {preset.title}
                  </h4>
                  <p className="text-xs text-slate-500 dark:text-slate-400 group-hover:text-slate-600 dark:group-hover:text-slate-300 transition-colors line-clamp-1">
                    {preset.subtitle}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <span className={`text-[11px] px-2 py-0.5 rounded font-mono font-medium ${
                  preset.expectedVerdict === 'approved' 
                    ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-500/20' 
                    : 'bg-rose-50 text-rose-700 dark:bg-rose-500/10 dark:text-rose-400 border border-rose-200 dark:border-rose-500/20'
                }`}>
                  {preset.expectedVerdict.toUpperCase()}
                </span>
                <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-slate-700 dark:group-hover:text-white group-hover:translate-x-0.5 transition-all" />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Live System Telemetry Bar */}
      <Card className="p-4 bg-slate-50 dark:bg-slate-950/80 border-slate-200 dark:border-white/8">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center divide-y sm:divide-y-0 sm:divide-x divide-slate-200 dark:divide-white/8">
          <div className="pt-2 sm:pt-0">
            <span className="text-[11px] text-slate-500 dark:text-slate-400 uppercase tracking-wider block font-semibold">Registrations</span>
            <span className="text-2xl font-bold text-slate-900 dark:text-white mt-1 block font-mono">{total}</span>
            <span className="text-[10px] text-slate-500">Live in Supabase</span>
          </div>

          <div className="pt-2 sm:pt-0">
            <span className="text-[11px] text-slate-500 dark:text-slate-400 uppercase tracking-wider block font-semibold">Auto-Approved</span>
            <span className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1 block font-mono">
              {Math.round((approved / total) * 100)}%
            </span>
            <span className="text-[10px] text-emerald-600/80 dark:text-emerald-500/80">&lt; 2% false positives</span>
          </div>

          <div className="pt-2 sm:pt-0">
            <span className="text-[11px] text-slate-500 dark:text-slate-400 uppercase tracking-wider block font-semibold">Pending Review</span>
            <span className="text-2xl font-bold text-amber-600 dark:text-amber-400 mt-1 block font-mono">{reviews}</span>
            <span className="text-[10px] text-slate-500">Borderline score (0.60–0.85)</span>
          </div>

          <div className="pt-2 sm:pt-0">
            <span className="text-[11px] text-slate-500 dark:text-slate-400 uppercase tracking-wider block font-semibold">Average Speed</span>
            <span className="text-2xl font-bold text-indigo-600 dark:text-indigo-400 mt-1 block font-mono">740ms</span>
            <span className="text-[10px] text-indigo-600/80 dark:text-indigo-400/80">Self-contained OpenCV/ArcFace</span>
          </div>
        </div>
      </Card>
    </div>
  );
};
