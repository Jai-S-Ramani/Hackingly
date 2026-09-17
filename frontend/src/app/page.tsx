'use client';

import React, { useEffect } from 'react';
import { Header } from '../components/layout/Header';
import { Sidebar } from '../components/layout/Sidebar';
import { PromptBar } from '../components/layout/PromptBar';
import { HeroHubView } from '../components/views/HeroHubView';
import { LiveFeedView } from '../components/views/LiveFeedView';
import { JudgeSandboxView } from '../components/views/JudgeSandboxView';
import { ApplicantPortalView } from '../components/views/ApplicantPortalView';
import { RulesAnalyticsView } from '../components/views/RulesAnalyticsView';
import { ForensicModal } from '../components/views/ForensicModal';
import { CommandPalette } from '../components/ui/CommandPalette';
import { useAppStore } from '../store/useAppStore';

export default function Home() {
  const { activeTab, fetchRegistrations, fetchTelemetry } = useAppStore();

  useEffect(() => {
    fetchRegistrations();
    fetchTelemetry();
  }, [fetchRegistrations, fetchTelemetry]);

  return (
    <div className="min-h-screen flex flex-col bg-[#090D16] text-slate-100 selection:bg-indigo-500/30 selection:text-indigo-200">
      {/* Background Ambient Radial Auras (Confluence Mesh Spec) */}
      <div 
        className="fixed inset-0 pointer-events-none z-0"
        style={{
          backgroundImage: `
            radial-gradient(ellipse at 15% 0%, rgba(99, 102, 241, 0.12) 0%, transparent 55%),
            radial-gradient(ellipse at 85% 0%, rgba(16, 185, 129, 0.10) 0%, transparent 55%)
          `
        }}
      />

      {/* Global Header */}
      <Header />

      {/* Main Workspace Frame: Sidebar + Content */}
      <div className="flex-1 flex w-full relative z-10 overflow-hidden">
        {/* Obsidian Sidebar */}
        <Sidebar />

        {/* Scrollable Center Canvas */}
        <main className="flex-1 overflow-y-auto pb-24">
          {activeTab === 'hub' && <HeroHubView />}
          {activeTab === 'feed' && <LiveFeedView />}
          {activeTab === 'sandbox' && <JudgeSandboxView />}
          {activeTab === 'portal' && <ApplicantPortalView />}
          {activeTab === 'analytics' && <RulesAnalyticsView />}
        </main>
      </div>

      {/* Confluence Floating Bottom Action Prompt Bar */}
      <PromptBar />

      {/* Modals & Dialogs */}
      <ForensicModal />
      <CommandPalette />
    </div>
  );
}
