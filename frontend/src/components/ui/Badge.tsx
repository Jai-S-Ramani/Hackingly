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
  const sizeStyles = size === 'sm' ? "text-[11px] px-2 py-0.5 gap-1" : "text-xs px-2.5 py-1 gap-1.5";

  let styles = "bg-white/5 text-slate-300 border-white/10";
  let icon = null;

  switch (status) {
    case 'approved':
      styles = "bg-emerald-500/10 text-emerald-400 border-emerald-500/30 dark:bg-emerald-950/40";
      icon = <CheckCircle2 className="w-3 h-3 text-emerald-400" aria-hidden="true" />;
      break;
    case 'manual_review':
      styles = "bg-amber-500/10 text-amber-400 border-amber-500/30 dark:bg-amber-950/40";
      icon = <AlertTriangle className="w-3 h-3 text-amber-400" aria-hidden="true" />;
      break;
    case 'rejected':
      styles = "bg-rose-500/10 text-rose-400 border-rose-500/30 dark:bg-rose-950/40";
      icon = <XCircle className="w-3 h-3 text-rose-400" aria-hidden="true" />;
      break;
    case 'duplicate':
      styles = "bg-rose-500/15 text-rose-300 border-rose-500/40 dark:bg-rose-950/60";
      icon = <Copy className="w-3 h-3 text-rose-400" aria-hidden="true" />;
      break;
    case 'sparkle':
      styles = "bg-indigo-500/10 text-indigo-300 border-indigo-500/30 backdrop-blur-md";
      icon = <Sparkles className="w-3 h-3 text-indigo-400" aria-hidden="true" />;
      break;
    case 'neutral':
    default:
      styles = "bg-slate-800/60 text-slate-300 border-slate-700/60";
      icon = <ShieldCheck className="w-3 h-3 text-slate-400" aria-hidden="true" />;
      break;
  }

  const displayText = label || (typeof children === 'string' ? children : status.replace('_', ' ').toUpperCase());

  return (
    <span className={`inline-flex items-center font-medium rounded-full border tracking-wide select-none ${sizeStyles} ${styles} ${className}`}>
      {icon}
      <span>{children || displayText}</span>
    </span>
  );
};
