'use client';

import React, { useEffect } from 'react';
import { 
  Search, 
  Eye, 
  Check, 
  X, 
  Clock, 
  AlertTriangle,
  RefreshCw
} from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';

export const LiveFeedView: React.FC = () => {
  const { 
    registrations, 
    isLoading, 
    fetchRegistrations, 
    statusFilter, 
    setStatusFilter,
    searchQuery,
    setSearchQuery,
    setSelectedRegistration,
    updateReviewDecision
  } = useAppStore();

  useEffect(() => {
    fetchRegistrations();
  }, [fetchRegistrations]);

  const filterTabs = [
    { id: 'all', label: 'All Submissions' },
    { id: 'manual_review', label: 'Manual Review' },
    { id: 'approved', label: 'Approved' },
    { id: 'rejected', label: 'Fraud / Mismatches' },
  ];

  return (
    <div className="max-w-5xl mx-auto px-4 py-6 space-y-6 select-none animate-in fade-in duration-200">
      {/* Header & Filter Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight flex items-center gap-2">
            <span>Live Registration Feed</span>
            <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-700 dark:text-indigo-400 border border-indigo-500/20 font-mono font-semibold">
              {registrations.length} Records
            </span>
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Real-time feed of submitted participant IDs streaming directly from Supabase.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button 
            size="sm" 
            variant="outline" 
            onClick={() => fetchRegistrations()}
            isLoading={isLoading}
            leftIcon={<RefreshCw className="w-3.5 h-3.5" />}
          >
            Refresh Feed
          </Button>
        </div>
      </div>

      {/* Search & Filter Tabs Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 p-2 rounded-xl bg-slate-100/90 dark:bg-slate-900/60 border border-slate-200 dark:border-white/8 backdrop-blur-md">
        {/* Search Input */}
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search by participant name, masked ID, or ID type..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 bg-white dark:bg-slate-950/60 border border-slate-300 dark:border-white/8 rounded-lg text-xs text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:outline-none focus:border-indigo-500"
          />
        </div>

        {/* Filter Tabs */}
        <div className="flex items-center gap-1 overflow-x-auto pb-1 sm:pb-0">
          {filterTabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setStatusFilter(tab.id)}
              className={`px-2.5 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors cursor-pointer ${
                statusFilter === tab.id
                  ? 'bg-white text-slate-900 border border-slate-300 shadow-sm dark:bg-white/10 dark:text-white dark:border-white/15 dark:shadow-none'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:bg-white/5 border border-transparent'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Registration Cards Feed */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-24 rounded-xl bg-slate-100 dark:bg-slate-900/40 border border-slate-200 dark:border-white/5 animate-pulse" />
          ))}
        </div>
      ) : registrations.length === 0 ? (
        <Card className="p-8 text-center space-y-3">
          <AlertTriangle className="w-8 h-8 text-amber-500 mx-auto" />
          <h3 className="text-sm font-semibold text-slate-900 dark:text-white">No registrations found</h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 max-w-sm mx-auto">
            No applicant records matched your search query or filter. Try clearing filters or running a test submission in the Judge Sandbox.
          </p>
          <Button size="sm" variant="secondary" onClick={() => { setStatusFilter('all'); setSearchQuery(''); }}>
            Reset Filters
          </Button>
        </Card>
      ) : (
        <div className="space-y-3">
          {registrations.map((reg) => (
            <Card
              key={reg.id}
              className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-slate-200/90 dark:border-white/8 hover:border-slate-300 dark:hover:border-white/15 transition-all group"
            >
              {/* Left Column: Avatar & Basic Info */}
              <div className="flex items-start sm:items-center gap-3.5">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-slate-200 to-slate-300 dark:from-slate-800 dark:to-slate-700 border border-slate-300 dark:border-white/10 flex items-center justify-center text-slate-800 dark:text-white font-bold text-xs flex-shrink-0">
                  {reg.full_name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()}
                </div>

                <div className="space-y-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-sm font-semibold text-slate-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-300 transition-colors">
                      {reg.full_name}
                    </span>
                    <Badge status={reg.decision} />
                    <span className="text-[11px] px-2 py-0.5 rounded bg-slate-100 dark:bg-white/5 text-slate-600 dark:text-slate-400 font-mono border border-slate-200 dark:border-white/5 uppercase font-medium">
                      {reg.id_type}
                    </span>
                  </div>

                  <div className="flex flex-wrap items-center gap-3 text-xs text-slate-600 dark:text-slate-400">
                    <span className="font-mono text-slate-800 dark:text-slate-300 font-medium">{reg.id_number_masked}</span>
                    {reg.dob && <span>DOB: {reg.dob}</span>}
                    <span className="flex items-center gap-1 text-[11px] text-slate-500">
                      <Clock className="w-3 h-3" />
                      {new Date(reg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>

                  {/* Reasons Preview */}
                  {reg.reasons && reg.reasons.length > 0 && (
                    <p className="text-[11px] text-slate-500 dark:text-slate-400 line-clamp-1 pt-0.5">
                      {reg.reasons[0]}
                    </p>
                  )}
                </div>
              </div>

              {/* Right Column: Score & Action Buttons */}
              <div className="flex items-center justify-between sm:justify-end gap-3 pt-2 sm:pt-0 border-t sm:border-t-0 border-slate-100 dark:border-white/5">
                {/* Confidence Meter */}
                <div className="text-right">
                  <span className="text-[10px] text-slate-500 uppercase tracking-wider block font-semibold">Confidence</span>
                  <span className={`text-base font-bold font-mono ${
                    reg.confidence >= 0.85 ? 'text-emerald-600 dark:text-emerald-400' :
                    reg.confidence >= 0.60 ? 'text-amber-600 dark:text-amber-400' : 'text-rose-600 dark:text-rose-400'
                  }`}>
                    {Math.round(reg.confidence * 100)}%
                  </span>
                </div>

                {/* Inspect Button */}
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={() => setSelectedRegistration(reg)}
                  leftIcon={<Eye className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />}
                >
                  Inspect
                </Button>

                {/* Inline Quick Action Buttons for Manual Review */}
                {reg.decision === 'manual_review' && (
                  <div className="flex items-center gap-1">
                    <button
                      onClick={() => updateReviewDecision(reg.id, 'approved', 'Approved by lead organizer in feed')}
                      aria-label="Approve registration"
                      className="p-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30 transition-colors cursor-pointer"
                    >
                      <Check className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => updateReviewDecision(reg.id, 'rejected', 'Rejected due to failed identity verification')}
                      aria-label="Reject registration"
                      className="p-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-600 dark:text-rose-400 border border-rose-500/30 transition-colors cursor-pointer"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
