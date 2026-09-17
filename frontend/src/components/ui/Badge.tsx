'use client';

import React from 'react';
import { CheckCircle2, AlertTriangle, XCircle, Sparkles, Copy, ShieldCheck } from 'lucide-react';
import { DecisionStatus } from '../../services/types';

export interface BadgeProps {
  status?: DecisionStatus | 'duplicate' | 'sparkle' | 'neutral';
  label?: string;
  size?: 'sm' | 'md';
  className?: string;
  children?: React.ReactNode;
}

export const Badge: React.FC<BadgeProps> = ({
  status = 'neutral',
  label,
  size = 'md',
  className = '',
  children
}) => {
  const sizeStyles = size === 'sm' ? "text-[11px] px-2 py-0.5 gap-1 font-medium" : "text-xs px-2.5 py-1 gap-1.5 font-medium";

  let styles = "bg-slate-100 text-slate-700 border-slate-200 dark:bg-white/5 dark:text-slate-300 dark:border-white/10";
  let icon = null;

  switch (status) {
    case 'approved':
      styles = "bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-500/10 dark:text-emerald-400 dark:border-emerald-500/30";
      icon = <CheckCircle2 className="w-3 h-3 text-emerald-600 dark:text-emerald-400" aria-hidden="true" />;
      break;
    case 'manual_review':
      styles = "bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-500/10 dark:text-amber-400 dark:border-amber-500/30";
      icon = <AlertTriangle className="w-3 h-3 text-amber-600 dark:text-amber-400" aria-hidden="true" />;
      break;
    case 'rejected':
      styles = "bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-500/10 dark:text-rose-400 dark:border-rose-500/30";
      icon = <XCircle className="w-3 h-3 text-rose-600 dark:text-rose-400" aria-hidden="true" />;
      break;
    case 'duplicate':
      styles = "bg-rose-100 text-rose-800 border-rose-300 dark:bg-rose-500/15 dark:text-rose-300 dark:border-rose-500/40";
      icon = <Copy className="w-3 h-3 text-rose-600 dark:text-rose-400" aria-hidden="true" />;
      break;
    case 'sparkle':
      styles = "bg-indigo-50 text-indigo-700 border-indigo-200 dark:bg-indigo-500/10 dark:text-indigo-300 dark:border-indigo-500/30 backdrop-blur-md";
      icon = <Sparkles className="w-3 h-3 text-indigo-600 dark:text-indigo-400" aria-hidden="true" />;
      break;
    case 'neutral':
    default:
      styles = "bg-slate-100 text-slate-700 border-slate-200 dark:bg-slate-800/60 dark:text-slate-300 dark:border-slate-700/60";
      icon = <ShieldCheck className="w-3 h-3 text-slate-500 dark:text-slate-400" aria-hidden="true" />;
      break;
  }

  const displayText = label || (typeof children === 'string' ? children : status.replace('_', ' ').toUpperCase());

  return (
    <span className={`inline-flex items-center rounded-full border tracking-wide select-none ${sizeStyles} ${styles} ${className}`}>
      {icon}
      <span>{children || displayText}</span>
    </span>
  );
};
