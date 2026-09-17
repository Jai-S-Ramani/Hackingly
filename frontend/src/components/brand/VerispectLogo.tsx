'use client';

import React from 'react';
import { motion, useReducedMotion } from 'framer-motion';

export type LogoVariant = 'primary' | 'symbol' | 'horizontal' | 'monochrome';
export type LogoStatus = 'default' | 'loading' | 'success' | 'error' | 'empty';

interface VerispectLogoProps {
  variant?: LogoVariant;
  status?: LogoStatus;
  size?: number;
  className?: string;
  showTagline?: boolean;
  animated?: boolean;
}

export const VerispectLogo: React.FC<VerispectLogoProps> = ({
  variant = 'primary',
  status = 'default',
  size = 36,
  className = '',
  showTagline = false,
  animated = true,
}) => {
  const shouldReduceMotion = useReducedMotion();
  const isAnimated = animated && !shouldReduceMotion;

  // Status color mapping
  const statusColors = {
    default: {
      primary: '#4F46E5', // Indigo
      accent: '#06B6D4',  // Cyan
      node: '#38BDF8',    // Sky
      glow: 'rgba(6, 182, 212, 0.45)',
    },
    loading: {
      primary: '#6366F1',
      accent: '#818CF8',
      node: '#A5B4FC',
      glow: 'rgba(99, 102, 241, 0.5)',
    },
    success: {
      primary: '#059669', // Emerald
      accent: '#10B981',
      node: '#34D399',
      glow: 'rgba(16, 185, 129, 0.5)',
    },
    error: {
      primary: '#DC2626', // Crimson
      accent: '#EF4444',
      node: '#F87171',
      glow: 'rgba(239, 68, 68, 0.5)',
    },
    empty: {
      primary: '#64748B', // Slate
      accent: '#94A3B8',
      node: '#CBD5E1',
      glow: 'rgba(148, 163, 184, 0.2)',
    },
    monochrome: {
      primary: 'currentColor',
      accent: 'currentColor',
      node: 'currentColor',
      glow: 'none',
    },
  };

  const currentColors = variant === 'monochrome' ? statusColors.monochrome : statusColors[status];

  // The Forensic Aperture Icon
  const LogoIcon = (
    <svg
      width={size}
      height={size}
      viewBox="0 0 48 48"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="shrink-0 transition-transform duration-300 group-hover:scale-105"
      role="img"
      aria-labelledby={`verispect-logo-title-${status}`}
    >
      <title id={`verispect-logo-title-${status}`}>Verispect Forensic Verification Glyph</title>
      <desc>Precision geometric lens framing a verification node with cryptographic alignment ticks</desc>

      <defs>
        <linearGradient id={`verispect-bracket-grad-${status}`} x1="4" y1="4" x2="44" y2="44" gradientUnits="userSpaceOnUse">
          <stop stopColor={currentColors.primary} />
          <stop offset="1" stopColor={currentColors.accent} />
        </linearGradient>
        <radialGradient id={`verispect-glow-${status}`} cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor={currentColors.node} stopOpacity="0.8" />
          <stop offset="100%" stopColor={currentColors.accent} stopOpacity="0" />
        </radialGradient>
      </defs>

      {/* Subtle background glow */}
      {status !== 'empty' && variant !== 'monochrome' && (
        <circle cx="24" cy="24" r="16" fill={`url(#verispect-glow-${status})`} opacity="0.35" />
      )}

      {/* Precision Frame Brackets: Top-Left Aperture */}
      <motion.path
        d="M 6 18 L 6 10 C 6 7.79 7.79 6 10 6 L 18 6"
        stroke={`url(#verispect-bracket-grad-${status})`}
        strokeWidth="3.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        initial={isAnimated ? { pathLength: 0, opacity: 0 } : false}
        animate={isAnimated ? { pathLength: 1, opacity: 1 } : false}
        transition={{ duration: 0.6, ease: 'easeOut' }}
      />

      {/* Precision Frame Brackets: Bottom-Right Aperture */}
      <motion.path
        d="M 42 30 L 42 38 C 42 40.21 40.21 42 38 42 L 30 42"
        stroke={`url(#verispect-bracket-grad-${status})`}
        strokeWidth="3.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        initial={isAnimated ? { pathLength: 0, opacity: 0 } : false}
        animate={isAnimated ? { pathLength: 1, opacity: 1 } : false}
        transition={{ duration: 0.6, delay: 0.1, ease: 'easeOut' }}
      />

      {/* Forensic Reticle Crosshairs / Alignment Ticks */}
      <line x1="24" y1="8" x2="24" y2="12" stroke={currentColors.accent} strokeWidth="2" strokeLinecap="round" opacity="0.75" />
      <line x1="24" y1="36" x2="24" y2="40" stroke={currentColors.accent} strokeWidth="2" strokeLinecap="round" opacity="0.75" />
      <line x1="8" y1="24" x2="12" y2="24" stroke={currentColors.accent} strokeWidth="2" strokeLinecap="round" opacity="0.75" />
      <line x1="36" y1="24" x2="40" y2="24" stroke={currentColors.accent} strokeWidth="2" strokeLinecap="round" opacity="0.75" />

      {/* Central Verification Node */}
      <motion.rect
        x="17"
        y="17"
        width="14"
        height="14"
        rx="3.5"
        transform="rotate(45 24 24)"
        fill={currentColors.node}
        initial={isAnimated ? { scale: 0.7, opacity: 0 } : false}
        animate={
          isAnimated && status === 'loading'
            ? { scale: [0.85, 1.1, 0.85], opacity: [0.7, 1, 0.7] }
            : isAnimated
            ? { scale: 1, opacity: 1 }
            : false
        }
        transition={
          status === 'loading'
            ? { repeat: Infinity, duration: 1.4, ease: 'easeInOut' }
            : { duration: 0.4, delay: 0.25 }
        }
      />

      {/* Internal Security Node Core */}
      <circle cx="24" cy="24" r="2.5" fill="#FFFFFF" />

      {/* Dynamic scanline when loading */}
      {status === 'loading' && isAnimated && (
        <motion.line
          x1="12"
          y1="14"
          x2="36"
          y2="14"
          stroke="#FFFFFF"
          strokeWidth="1.5"
          strokeLinecap="round"
          animate={{ y1: [14, 34, 14], y2: [14, 34, 14] }}
          transition={{ repeat: Infinity, duration: 1.8, ease: 'easeInOut' }}
        />
      )}
    </svg>
  );

  if (variant === 'symbol') {
    return <div className={`inline-flex items-center justify-center ${className}`}>{LogoIcon}</div>;
  }

  return (
    <div className={`inline-flex items-center gap-2.5 ${className}`}>
      {LogoIcon}
      <div className="flex flex-col">
        <div className="flex items-center gap-1.5">
          <span className="text-lg font-bold tracking-tight text-slate-900 dark:text-white font-mono">
            VERISPECT
          </span>
          <span className="rounded bg-indigo-500/10 px-1.5 py-0.5 text-[10px] font-semibold text-indigo-600 dark:text-indigo-400 border border-indigo-500/20">
            PRO
          </span>
        </div>
        {showTagline && (
          <span className="text-[10px] font-medium tracking-wider text-slate-500 dark:text-slate-400 uppercase font-mono">
            Forensic Intelligence
          </span>
        )}
      </div>
    </div>
  );
};
export default VerispectLogo;
