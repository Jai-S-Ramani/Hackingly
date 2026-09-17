'use client';

import React from 'react';

interface ConfidenceGaugeProps {
  score: number; // 0.0 to 1.0 or 0 to 100
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  className?: string;
}

export const ConfidenceGauge: React.FC<ConfidenceGaugeProps> = ({
  score,
  size = 'md',
  showLabel = true,
  className = '',
}) => {
  // Normalize score to 0..100
  const val = score <= 1.0 ? Math.round(score * 100) : Math.min(100, Math.round(score));

  let colorClass = 'text-emerald-500 stroke-emerald-500';
  let badgeBg = 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20';

  if (val < 60) {
    colorClass = 'text-rose-500 stroke-rose-500';
    badgeBg = 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/20';
  } else if (val < 85) {
    colorClass = 'text-amber-500 stroke-amber-500';
    badgeBg = 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20';
  }

  const dimension = { sm: 28, md: 40, lg: 54 }[size];
  const strokeWidth = { sm: 3, md: 4, lg: 5 }[size];
  const radius = (dimension - strokeWidth * 2) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (val / 100) * circumference;

  return (
    <div className={`inline-flex items-center gap-2 ${className}`}>
      <div className="relative inline-flex items-center justify-center shrink-0">
        <svg width={dimension} height={dimension} className="transform -rotate-90">
          <circle
            cx={dimension / 2}
            cy={dimension / 2}
            r={radius}
            stroke="currentColor"
            strokeWidth={strokeWidth}
            className="text-slate-200 dark:text-white/10 fill-none"
          />
          <circle
            cx={dimension / 2}
            cy={dimension / 2}
            r={radius}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className={`${colorClass} fill-none transition-all duration-700 ease-out`}
          />
        </svg>
        <span className={`absolute font-mono font-bold ${size === 'sm' ? 'text-[9px]' : size === 'md' ? 'text-xs' : 'text-sm'} text-slate-800 dark:text-slate-200`}>
          {val}%
        </span>
      </div>
      {showLabel && (
        <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full border ${badgeBg}`}>
          {val >= 85 ? 'High Confidence' : val >= 60 ? 'Moderate' : 'Low Confidence'}
        </span>
      )}
    </div>
  );
};
