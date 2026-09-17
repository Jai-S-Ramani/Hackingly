'use client';

import React, { useEffect, useState } from 'react';
import { Sun, Moon, Search, Sparkles, Menu, X, Activity } from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { useThemeStore } from '../../store/useThemeStore';
import { VerispectLogo } from '../brand/VerispectLogo';
import { verificationService } from '../../services';

export const Header: React.FC = () => {
  const { 
    activeTab, 
    setActiveTab, 
    setCommandPaletteOpen, 
    registrations,
    mobileMenuOpen,
    setMobileMenuOpen
  } = useAppStore();
  const { theme, toggleTheme } = useThemeStore();
  const [healthStatus, setHealthStatus] = useState<{ status: string; database: string }>({
    status: 'checking',
    database: 'sqlite'
  });

  useEffect(() => {
    let isMounted = true;
    const checkHealth = async () => {
      try {
        const h = await verificationService.getHealth();
        if (isMounted) setHealthStatus(h);
      } catch {
        if (isMounted) setHealthStatus({ status: 'offline', database: 'fallback' });
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  const reviewCount = registrations.filter(r => r.decision === 'manual_review').length;

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200/80 dark:border-white/8 bg-white/85 dark:bg-slate-950/80 backdrop-blur-xl transition-colors duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <div className="flex items-center gap-3">
          {/* Mobile hamburger button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 -ml-2 rounded-lg text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5 cursor-pointer"
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>

          <div 
            onClick={() => setActiveTab('hub')} 
            className="cursor-pointer group flex items-center"
            role="button"
            tabIndex={0}
            onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') setActiveTab('hub'); }}
            aria-label="Go to Verispect Overview"
          >
            <VerispectLogo variant="primary" size={32} showTagline={false} />
          </div>
        </div>

        {/* Central Desktop Navigation Tabs */}
        <nav className="hidden md:flex items-center gap-1 text-sm font-medium" aria-label="Main Navigation">
          <button
            onClick={() => setActiveTab('hub')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
              activeTab === 'hub' 
                ? 'text-slate-900 bg-slate-100 font-semibold dark:text-white dark:bg-white/10 shadow-xs' 
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/60 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:bg-white/5'
            }`}
          >
            Command Center
          </button>
          <button
            onClick={() => setActiveTab('feed')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer flex items-center gap-1.5 ${
              activeTab === 'feed' 
                ? 'text-slate-900 bg-slate-100 font-semibold dark:text-white dark:bg-white/10 shadow-xs' 
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/60 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:bg-white/5'
            }`}
          >
            <span>Live Audit Feed</span>
            {reviewCount > 0 && (
              <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-amber-500/20 text-amber-700 dark:text-amber-300 border border-amber-500/30 font-semibold">
                {reviewCount}
              </span>
            )}
          </button>
          <button
            onClick={() => setActiveTab('sandbox')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer flex items-center gap-1.5 ${
              activeTab === 'sandbox' 
                ? 'text-slate-900 bg-slate-100 font-semibold dark:text-white dark:bg-white/10 shadow-xs' 
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/60 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:bg-white/5'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5 text-indigo-500 dark:text-indigo-400" />
            <span>Judge Sandbox</span>
          </button>
          <button
            onClick={() => setActiveTab('portal')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
              activeTab === 'portal' 
                ? 'text-slate-900 bg-slate-100 font-semibold dark:text-white dark:bg-white/10 shadow-xs' 
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/60 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:bg-white/5'
            }`}
          >
            Applicant Portal
          </button>
          <button
            onClick={() => setActiveTab('analytics')}
            className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
              activeTab === 'analytics' 
                ? 'text-slate-900 bg-slate-100 font-semibold dark:text-white dark:bg-white/10 shadow-xs' 
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/60 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:bg-white/5'
            }`}
          >
            Rules & Policy Engine
          </button>
        </nav>

        {/* Right Actions & Health Telemetry */}
        <div className="flex items-center gap-2 sm:gap-2.5">
          {/* Real Backend Health Status Pill */}
          <div 
            title={`Backend Status: ${healthStatus.status} | Storage: ${healthStatus.database}`}
            className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-100 dark:bg-white/5 border border-slate-200 dark:border-white/10 text-[11px] font-medium select-none"
          >
            <span className={`w-1.5 h-1.5 rounded-full ${healthStatus.status === 'ok' ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'}`} />
            <span className="font-mono text-slate-700 dark:text-slate-300">
              {healthStatus.status === 'ok' ? (healthStatus.database === 'supabase' ? 'Supabase Cloud' : 'FastAPI Active') : 'Offline Mode'}
            </span>
          </div>

          {/* Command Palette Launcher */}
          <button
            onClick={() => setCommandPaletteOpen(true)}
            className="flex items-center gap-2 px-2.5 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200/70 border border-slate-200 dark:text-slate-400 dark:hover:text-white dark:bg-white/5 dark:hover:bg-white/10 dark:border-white/10 text-xs transition-colors cursor-pointer"
            aria-label="Search or run command (Command + K)"
          >
            <Search className="w-3.5 h-3.5" />
            <span className="hidden lg:inline">Quick Action</span>
            <kbd className="text-[10px] px-1.5 py-0.5 rounded bg-slate-200 dark:bg-white/10 text-slate-700 dark:text-slate-300 font-mono">⌘K</kbd>
          </button>

          {/* Theme Switcher */}
          <button
            onClick={toggleTheme}
            aria-label="Toggle dark and light theme"
            className="p-2 rounded-lg border border-slate-200 hover:bg-slate-100 text-slate-600 hover:text-slate-900 dark:border-white/10 dark:text-slate-400 dark:hover:text-white dark:hover:bg-white/5 transition-colors cursor-pointer"
          >
            {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-indigo-600" />}
          </button>
        </div>
      </div>

      {/* Responsive Mobile Navigation Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-200 dark:border-white/10 bg-white/95 dark:bg-slate-950/95 backdrop-blur-xl px-4 py-3 space-y-1 animate-in slide-in-from-top-2 duration-150">
          <button
            onClick={() => setActiveTab('hub')}
            className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium ${
              activeTab === 'hub' ? 'bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 font-bold' : 'text-slate-700 dark:text-slate-300'
            }`}
          >
            <span>Command Center</span>
          </button>
          <button
            onClick={() => setActiveTab('feed')}
            className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium ${
              activeTab === 'feed' ? 'bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 font-bold' : 'text-slate-700 dark:text-slate-300'
            }`}
          >
            <span>Live Audit Feed</span>
            {reviewCount > 0 && (
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-700 dark:text-amber-300 font-bold">
                {reviewCount}
              </span>
            )}
          </button>
          <button
            onClick={() => setActiveTab('sandbox')}
            className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium ${
              activeTab === 'sandbox' ? 'bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 font-bold' : 'text-slate-700 dark:text-slate-300'
            }`}
          >
            <span>Judge Sandbox</span>
            <Sparkles className="w-4 h-4 text-indigo-500" />
          </button>
          <button
            onClick={() => setActiveTab('portal')}
            className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium ${
              activeTab === 'portal' ? 'bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 font-bold' : 'text-slate-700 dark:text-slate-300'
            }`}
          >
            <span>Applicant Portal</span>
          </button>
          <button
            onClick={() => setActiveTab('analytics')}
            className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium ${
              activeTab === 'analytics' ? 'bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 font-bold' : 'text-slate-700 dark:text-slate-300'
            }`}
          >
            <span>Rules & Policy Engine</span>
          </button>
        </div>
      )}
    </header>
  );
};
export default Header;
