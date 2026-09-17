'use client';

import React from 'react';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  hoverable?: boolean;
  bordered?: boolean;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(({
  children,
  hoverable = false,
  bordered = true,
  className = '',
  ...props
}, ref) => {
  const baseStyles = "rounded-xl bg-white dark:bg-slate-900/60 backdrop-blur-md transition-all duration-200";
  const borderStyles = bordered ? "border border-slate-200/90 dark:border-white/8 shadow-sm shadow-slate-900/5 dark:shadow-none" : "";
  const hoverStyles = hoverable ? "hover:border-slate-300 dark:hover:border-white/20 hover:bg-slate-50/80 dark:hover:bg-slate-800/60 hover:shadow-md dark:hover:shadow-xl hover:shadow-indigo-500/5 cursor-pointer" : "";

  return (
    <div
      ref={ref}
      className={`${baseStyles} ${borderStyles} ${hoverStyles} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
});

Card.displayName = 'Card';
