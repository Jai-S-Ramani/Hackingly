'use client';

import React, { useState } from 'react';
import { 
  PlayCircle, 
  Terminal, 
  Cpu
} from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { mockJudgePresets } from '../../services/mockData';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Badge } from '../ui/Badge';
import { verificationService } from '../../services';

export const JudgeSandboxView: React.FC = () => {
  const { activePreset, setActivePreset, setSelectedRegistration, fetchRegistrations } = useAppStore();
  const [selectedPreset, setSelectedPreset] = useState(activePreset || mockJudgePresets[0]);
  const [isRunning, setIsRunning] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [result, setResult] = useState<any>(null);

  const handleRunSimulation = async () => {
    setIsRunning(true);
    setResult(null);
    setLogs([]);

    const steps = [
      `[1/5] Ingesting document & selfie for ${selectedPreset.name}...`,
      `[2/5] Stage 1 Quality: Analyzing Laplacian variance & EXIF metadata...`,
      `[3/5] Stage 2 OCR: Extracting fields and validating Verhoeff checksum for ${selectedPreset.idType.toUpperCase()}...`,
      `[4/5] Stage 3 Biometrics: Running DeepFace ArcFace facial embedding comparison...`,
      `[5/5] Stage 4 Duplicate: Computing salted SHA-256 hash collision check in Supabase...`,
      `[Complete] Stage 5 Decision: Evaluated rules. Generating final autonomous verdict.`
    ];

    for (let i = 0; i < steps.length; i++) {
      await new Promise(res => setTimeout(res, 180));
      setLogs(prev => [...prev, steps[i]]);
    }

    const formData = new FormData();
    formData.append("name", selectedPreset.name);
    formData.append("id_type", selectedPreset.idType);
    formData.append("id_number", selectedPreset.idNumber);
    formData.append("dob", selectedPreset.dob);
    formData.append("event_id", selectedPreset.eventId);

    const res = await verificationService.verifySubmission(formData);
    setResult(res);
    setIsRunning(false);
    await fetchRegistrations();
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-6 space-y-6 select-none animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
              Judge Interactive Sandbox
            </h2>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/30 font-semibold">
              Live Stage Demo
            </span>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Test autonomous pipeline execution in real-time with 1-click forensic scenarios.
          </p>
        </div>

        <Button
          variant="primary"
          onClick={handleRunSimulation}
          isLoading={isRunning}
          leftIcon={<PlayCircle className="w-4 h-4" />}
        >
          Run Autonomous Verification
        </Button>
      </div>

      {/* Preset Selector Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {mockJudgePresets.map((preset) => {
          const isSelected = selectedPreset.id === preset.id;
          return (
            <div
              key={preset.id}
              onClick={() => {
                setSelectedPreset(preset);
                setActivePreset(preset);
                setResult(null);
                setLogs([]);
              }}
              className={`p-3.5 rounded-xl border transition-all cursor-pointer flex flex-col justify-between shadow-sm dark:shadow-none ${
                isSelected
                  ? 'bg-indigo-50/80 dark:bg-slate-800/90 border-indigo-500/60 shadow-md shadow-indigo-500/10'
                  : 'bg-white dark:bg-slate-900/60 border-slate-200 dark:border-white/8 hover:border-slate-300 dark:hover:border-white/20 hover:bg-slate-50 dark:hover:bg-slate-900/90'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded uppercase font-semibold ${
                    preset.expectedVerdict === 'approved' 
                      ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400 border border-emerald-200 dark:border-transparent' 
                      : 'bg-rose-50 text-rose-700 dark:bg-rose-500/10 dark:text-rose-400 border border-rose-200 dark:border-transparent'
                  }`}>
                    {preset.expectedVerdict}
                  </span>
                  <span className="text-[10px] text-slate-500 uppercase font-semibold">{preset.category}</span>
                </div>
                <h3 className="text-sm font-bold text-slate-900 dark:text-white tracking-tight">{preset.title.split(':')[1]}</h3>
                <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1 line-clamp-2">{preset.subtitle}</p>
              </div>

              <div className="mt-3 pt-2 border-t border-slate-100 dark:border-white/5 flex items-center justify-between text-[11px] text-slate-600 dark:text-slate-400 font-mono">
                <span className="font-semibold">{preset.name}</span>
                <span className="text-slate-500">{preset.idType.toUpperCase()}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Main Execution Arena */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Terminal Stream (7 cols) */}
        <div className="lg:col-span-7">
          <Card className="p-4 bg-slate-950 border-slate-800 dark:border-white/10 font-mono text-xs flex flex-col h-80 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-white/8 mb-3 text-slate-400">
              <div className="flex items-center gap-2">
                <Terminal className="w-4 h-4 text-indigo-400" />
                <span className="text-white font-semibold">Autonomous Verification Pipeline Trace</span>
              </div>
              <span className="text-[10px] text-slate-500">Latency: ~740ms</span>
            </div>

            <div className="flex-1 overflow-y-auto space-y-1.5 text-slate-300">
              <div className="text-slate-500">// Ready to execute multi-agent verification pipeline</div>
              <div className="text-indigo-400">// Selected preset: {selectedPreset.title}</div>
              <div className="text-slate-400">// Applicant: {selectedPreset.name} ({selectedPreset.idType.toUpperCase()})</div>
              
              {logs.map((log, index) => (
                <div key={index} className="text-emerald-400 animate-in fade-in duration-150">
                  {log}
                </div>
              ))}

              {isRunning && (
                <div className="text-amber-400 animate-pulse">
                  &gt; Ingesting biometric embeddings and computing distance vectors...
                </div>
              )}
            </div>
          </Card>
        </div>

        {/* Live Verdict & Breakdown Card (5 cols) */}
        <div className="lg:col-span-5">
          <Card className="p-5 h-80 flex flex-col justify-between border-slate-200 dark:border-white/10 shadow-sm dark:shadow-none">
            <div>
              <span className="text-[11px] text-slate-500 dark:text-slate-400 uppercase tracking-wider block font-semibold">
                Autonomous Verification Verdict
              </span>

              {result ? (
                <div className="mt-4 space-y-3 animate-in zoom-in-95 duration-200">
                  <div className="flex items-center justify-between">
                    <Badge status={result.decision} size="md" />
                    <span className="text-2xl font-bold font-mono text-slate-900 dark:text-white">
                      {Math.round(result.confidence * 100)}%
                    </span>
                  </div>

                  <div className="space-y-1 text-xs pt-2 border-t border-slate-100 dark:border-white/8">
                    <span className="text-[10px] text-slate-500 uppercase tracking-wider block font-semibold">Decision Rationale</span>
                    <p className="text-slate-800 dark:text-slate-200 leading-relaxed font-medium">
                      {result.reasons?.[0] || "All checks satisfied."}
                    </p>
                  </div>

                  <div className="grid grid-cols-2 gap-2 pt-2 text-[11px] font-mono">
                    <div className="p-2 rounded-lg bg-slate-50 dark:bg-white/5 border border-slate-200 dark:border-white/5">
                      <span className="text-slate-500 block text-[10px]">VERHOEFF</span>
                      <span className="text-emerald-600 dark:text-emerald-400 font-semibold">VALID</span>
                    </div>
                    <div className="p-2 rounded-lg bg-slate-50 dark:bg-white/5 border border-slate-200 dark:border-white/5">
                      <span className="text-slate-500 block text-[10px]">ARCFACE</span>
                      <span className={result.decision === 'approved' ? 'text-emerald-600 dark:text-emerald-400 font-semibold' : 'text-rose-600 dark:text-rose-400 font-semibold'}>
                        {result.decision === 'approved' ? '94.8% MATCH' : 'MISMATCH'}
                      </span>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="mt-12 text-center space-y-2 text-slate-400 dark:text-slate-500">
                  <Cpu className="w-8 h-8 mx-auto text-slate-400 dark:text-slate-600 animate-bounce" />
                  <p className="text-xs">Click "Run Autonomous Verification" to execute live demo pipeline.</p>
                </div>
              )}
            </div>

            <div className="pt-3 border-t border-slate-100 dark:border-white/8">
              <Button
                variant="outline"
                size="sm"
                fullWidth
                disabled={!result}
                onClick={() => {
                  setSelectedRegistration({
                    id: result.registration_id,
                    event_id: selectedPreset.eventId,
                    full_name: selectedPreset.name,
                    id_type: selectedPreset.idType,
                    id_number_masked: `XXXX-XXXX-${selectedPreset.idNumber.slice(-4)}`,
                    dob: selectedPreset.dob,
                    decision: result.decision,
                    confidence: result.confidence,
                    reasons: result.reasons,
                    created_at: new Date().toISOString(),
                    breakdown: result.breakdown
                  });
                }}
              >
                Inspect Biometrics & ELA Heatmap
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
