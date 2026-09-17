'use client';

import React, { useState, useEffect } from 'react';
import { Search, ShieldCheck, PlayCircle, UploadCloud, Moon, Sun, ArrowRight, UserCheck } from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { useThemeStore } from '../../store/useThemeStore';
import { mockJudgePresets } from '../../services/mockData';

export const CommandPalette: React.FC = () => {
  const { 
    commandPaletteOpen, 
    setCommandPaletteOpen, 
    setActiveTab, 
    setActivePreset, 
    registrations,
    setSelectedRegistration
  } = useAppStore();
  const { theme, toggleTheme } = useThemeStore();
  const [query, setQuery] = useState('');

  // Global Keyboard Listener for Cmd+K / Ctrl+K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setCommandPaletteOpen(!commandPaletteOpen);
      }
      if (e.key === 'Escape' && commandPaletteOpen) {
        setCommandPaletteOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [commandPaletteOpen, setCommandPaletteOpen]);

  if (!commandPaletteOpen) return null;

  const filteredPresets = mockJudgePresets.filter(p => 
    p.title.toLowerCase().includes(query.toLowerCase()) ||
    p.subtitle.toLowerCase().includes(query.toLowerCase())
  );

  const filteredApplicants = registrations.filter(r => 
    r.full_name.toLowerCase().includes(query.toLowerCase()) ||
    r.id_number_masked.toLowerCase().includes(query.toLowerCase())
  ).slice(0, 4);

  const handleSelectTab = (tab: any) => {
    setActiveTab(tab);
    setCommandPaletteOpen(false);
  };

  const handleSelectPreset = (preset: any) => {
    setActivePreset(preset);
    setActiveTab('sandbox');
    setCommandPaletteOpen(false);
  };

  const handleSelectApplicant = (applicant: any) => {
    setSelectedRegistration(applicant);
    setActiveTab('feed');
    setCommandPaletteOpen(false);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-24 px-4">
      <div 
        className="fixed inset-0 bg-black/80 backdrop-blur-sm"
        onClick={() => setCommandPaletteOpen(false)}
      />

      <div className="relative w-full max-w-xl rounded-xl bg-slate-900 border border-white/12 shadow-2xl overflow-hidden z-10 animate-in zoom-in-95 duration-150">
        {/* Search Input Bar */}
        <div className="flex items-center px-4 py-3.5 border-b border-white/8 gap-3">
          <Search className="w-5 h-5 text-slate-400" />
          <input
            autoFocus
            type="text"
            placeholder="Type a command or search applicants..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-transparent text-white placeholder:text-slate-500 text-sm focus:outline-none"
          />
          <kbd className="hidden sm:inline-block text-[11px] px-2 py-0.5 rounded bg-white/5 border border-white/10 text-slate-400">
            ESC
          </kbd>
        </div>

        {/* Action List */}
        <div className="max-h-96 overflow-y-auto p-2 space-y-1 text-sm">
          {/* Section: Navigation */}
          <div className="px-2 py-1 text-[11px] font-medium text-slate-500 uppercase tracking-wider">
            Navigation
          </div>

          <button
            onClick={() => handleSelectTab('feed')}
            className="w-full flex items-center justify-between px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-white/5 transition-colors cursor-pointer text-left"
          >
            <div className="flex items-center gap-2.5">
              <ShieldCheck className="w-4 h-4 text-indigo-400" />
              <span>Go to Live Registration Feed</span>
            </div>
            <ArrowRight className="w-3.5 h-3.5 text-slate-500" />
          </button>

          <button
            onClick={() => handleSelectTab('sandbox')}
            className="w-full flex items-center justify-between px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-white/5 transition-colors cursor-pointer text-left"
          >
            <div className="flex items-center gap-2.5">
              <PlayCircle className="w-4 h-4 text-emerald-400" />
              <span>Go to Judge Interactive Sandbox</span>
            </div>
            <ArrowRight className="w-3.5 h-3.5 text-slate-500" />
          </button>

          <button
            onClick={() => handleSelectTab('portal')}
            className="w-full flex items-center justify-between px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-white/5 transition-colors cursor-pointer text-left"
          >
            <div className="flex items-center gap-2.5">
              <UploadCloud className="w-4 h-4 text-amber-400" />
              <span>Go to Applicant ID Upload Portal</span>
            </div>
            <ArrowRight className="w-3.5 h-3.5 text-slate-500" />
          </button>

          {/* Section: Judge Presets */}
          {filteredPresets.length > 0 && (
            <>
              <div className="px-2 pt-3 pb-1 text-[11px] font-medium text-slate-500 uppercase tracking-wider">
                Judge Demo Scenarios
              </div>
              {filteredPresets.map((preset) => (
                <button
                  key={preset.id}
                  onClick={() => handleSelectPreset(preset)}
                  className="w-full flex items-center justify-between px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-white/5 transition-colors cursor-pointer text-left"
                >
                  <div className="flex items-center gap-2.5">
                    <span className="w-2 h-2 rounded-full bg-indigo-500" />
                    <span>{preset.title}</span>
                  </div>
                  <span className="text-xs text-slate-500">{preset.category}</span>
                </button>
              ))}
            </>
          )}

          {/* Section: Matching Applicants */}
          {filteredApplicants.length > 0 && (
            <>
              <div className="px-2 pt-3 pb-1 text-[11px] font-medium text-slate-500 uppercase tracking-wider">
                Matching Applicants
              </div>
              {filteredApplicants.map((app) => (
                <button
                  key={app.id}
                  onClick={() => handleSelectApplicant(app)}
                  className="w-full flex items-center justify-between px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-white/5 transition-colors cursor-pointer text-left"
                >
                  <div className="flex items-center gap-2.5">
                    <UserCheck className="w-4 h-4 text-slate-400" />
                    <span>{app.full_name}</span>
                    <span className="text-xs text-slate-500">{app.id_number_masked}</span>
                  </div>
                  <span className={`text-[11px] font-medium px-2 py-0.5 rounded ${
                    app.decision === 'approved' ? 'bg-emerald-500/10 text-emerald-400' :
                    app.decision === 'rejected' ? 'bg-rose-500/10 text-rose-400' : 'bg-amber-500/10 text-amber-400'
                  }`}>
                    {app.decision.toUpperCase()}
                  </span>
                </button>
              ))}
            </>
          )}

          {/* Section: Preferences */}
          <div className="px-2 pt-3 pb-1 text-[11px] font-medium text-slate-500 uppercase tracking-wider">
            Preferences
          </div>
          <button
            onClick={() => {
              toggleTheme();
              setCommandPaletteOpen(false);
            }}
            className="w-full flex items-center justify-between px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-white/5 transition-colors cursor-pointer text-left"
          >
            <div className="flex items-center gap-2.5">
              {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-indigo-400" />}
              <span>Switch to {theme === 'dark' ? 'Light' : 'Dark'} Theme</span>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
};
