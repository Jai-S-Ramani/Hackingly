'use client';

import React from 'react';
import { 
  Plus, 
  ShieldCheck, 
  AlertTriangle, 
  XCircle, 
  Layers, 
  PlayCircle, 
  Sparkles, 
  Sliders,
  Cpu
} from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { mockJudgePresets } from '../../services/mockData';

export const Sidebar: React.FC = () => {
  const { 
    activeTab, 
    setActiveTab, 
    registrations, 
    statusFilter, 
    setStatusFilter,
    setActivePreset 
  } = useAppStore();

  const total = registrations.length;
  const reviews = registrations.filter(r => r.decision === 'manual_review').length;
  const duplicates = registrations.filter(r => r.breakdown?.is_duplicate || r.decision === 'rejected').length;
  const approved = registrations.filter(r => r.decision === 'approved').length;

  const handleQueueClick = (status: string) => {
    setStatusFilter(status);
    setActiveTab('feed');
  };

  const handlePresetClick = (preset: any) => {
    setActivePreset(preset);
    setActiveTab('sandbox');
  };

  return (
    <aside className="w-64 flex-shrink-0 border-r border-slate-200/80 dark:border-white/8 bg-slate-50/75 dark:bg-slate-950/60 backdrop-blur-md flex flex-col justify-between p-3 hidden lg:flex select-none transition-colors duration-200" aria-label="Sidebar Navigation">
      <div className="space-y-4">
        {/* New Verification Action Button */}
        <button
          onClick={() => setActiveTab('portal')}
          className="w-full flex items-center justify-center gap-2 py-2.5 px-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold transition-all shadow-sm shadow-indigo-600/20 border border-indigo-500/30 cursor-pointer active:scale-[0.98]"
        >
          <Plus className="w-4 h-4" />
          <span>New Verification</span>
        </button>

        {/* Section: ACTIVE AUDIT QUEUES */}
        <div>
          <div className="px-2 py-1 text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider font-mono">
            Audit Queues
          </div>
          <div className="space-y-0.5 mt-1">
            <button
              onClick={() => handleQueueClick('all')}
              className={`w-full flex items-center justify-between px-2.5 py-2 rounded-xl text-xs transition-colors cursor-pointer text-left ${
                activeTab === 'feed' && statusFilter === 'all'
                  ? 'bg-slate-200/80 text-slate-900 font-semibold dark:bg-white/10 dark:text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:bg-white/5'
              }`}
            >
              <div className="flex items-center gap-2">
                <Layers className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />
                <span>All Submissions</span>
              </div>
              <span className="text-[11px] text-slate-500 dark:text-slate-400 font-mono font-medium">{total}</span>
            </button>

            <button
              onClick={() => handleQueueClick('manual_review')}
              className={`w-full flex items-center justify-between px-2.5 py-2 rounded-xl text-xs transition-colors cursor-pointer text-left ${
                activeTab === 'feed' && statusFilter === 'manual_review'
                  ? 'bg-slate-200/80 text-slate-900 font-semibold dark:bg-white/10 dark:text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:bg-white/5'
              }`}
            >
              <div className="flex items-center gap-2">
                <AlertTriangle className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
                <span>Manual Review</span>
              </div>
              {reviews > 0 && (
                <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-amber-500/20 text-amber-700 dark:text-amber-300 font-mono font-bold">
                  {reviews}
                </span>
              )}
            </button>

            <button
              onClick={() => handleQueueClick('rejected')}
              className={`w-full flex items-center justify-between px-2.5 py-2 rounded-xl text-xs transition-colors cursor-pointer text-left ${
                activeTab === 'feed' && statusFilter === 'rejected'
                  ? 'bg-slate-200/80 text-slate-900 font-semibold dark:bg-white/10 dark:text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:bg-white/5'
              }`}
            >
              <div className="flex items-center gap-2">
                <XCircle className="w-3.5 h-3.5 text-rose-600 dark:text-rose-400" />
                <span>Fraud & Mismatches</span>
              </div>
              <span className="text-[11px] text-slate-500 dark:text-slate-400 font-mono font-medium">{duplicates}</span>
            </button>

            <button
              onClick={() => handleQueueClick('approved')}
              className={`w-full flex items-center justify-between px-2.5 py-2 rounded-xl text-xs transition-colors cursor-pointer text-left ${
                activeTab === 'feed' && statusFilter === 'approved'
                  ? 'bg-slate-200/80 text-slate-900 font-semibold dark:bg-white/10 dark:text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:bg-white/5'
              }`}
            >
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
                <span>Auto-Approved</span>
              </div>
              <span className="text-[11px] text-slate-500 dark:text-slate-400 font-mono font-medium">{approved}</span>
            </button>
          </div>
        </div>

        {/* Section: JUDGE SCENARIO PRESETS */}
        <div>
          <div className="px-2 py-1 text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider flex items-center justify-between font-mono">
            <span>Judge Sandbox Scenarios</span>
            <Sparkles className="w-3 h-3 text-indigo-500" />
          </div>
          <div className="space-y-1 mt-1">
            {mockJudgePresets.map((p) => (
              <button
                key={p.id}
                onClick={() => handlePresetClick(p)}
                className="w-full flex flex-col px-2.5 py-1.5 rounded-xl text-left text-xs transition-colors cursor-pointer hover:bg-slate-200/50 dark:hover:bg-white/5 border border-transparent hover:border-slate-200 dark:hover:border-white/5 group"
              >
                <div className="flex items-center justify-between text-slate-700 dark:text-slate-300 group-hover:text-slate-900 dark:group-hover:text-white font-medium">
                  <div className="flex items-center gap-1.5 truncate">
                    <PlayCircle className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400 shrink-0" />
                    <span className="truncate">{p.title.split(':')[1] || p.title}</span>
                  </div>
                </div>
                <span className="text-[10px] text-slate-500 font-mono truncate mt-0.5 pl-5">
                  {p.category.toUpperCase()} · {p.name}
                </span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Operator & System Status Pill */}
      <div className="pt-3 border-t border-slate-200/80 dark:border-white/8 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center text-white text-[11px] font-bold shadow-xs">
            <Cpu className="w-4 h-4 text-white" />
          </div>
          <div className="flex flex-col">
            <span className="text-xs font-bold text-slate-800 dark:text-slate-200">SecOps Operator</span>
            <span className="text-[10px] text-slate-500 font-mono">Verispect Core v1.2</span>
          </div>
        </div>
        <button 
          onClick={() => setActiveTab('analytics')}
          aria-label="Event rules policy engine"
          className="p-1.5 rounded-lg text-slate-500 hover:text-slate-900 hover:bg-slate-200/60 dark:text-slate-400 dark:hover:text-white dark:hover:bg-white/5 transition-colors cursor-pointer"
        >
          <Sliders className="w-4 h-4" />
        </button>
      </div>
    </aside>
  );
};
export default Sidebar;
