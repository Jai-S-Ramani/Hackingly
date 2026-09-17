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
  const baseStyles = "rounded-xl bg-slate-900/60 backdrop-blur-md dark:bg-slate-900/80 transition-all duration-200";
  const borderStyles = bordered ? "border border-white/8 dark:border-white/10" : "";
  const hoverStyles = hoverable ? "hover:border-white/20 hover:bg-slate-800/60 hover:shadow-xl hover:shadow-indigo-500/5 cursor-pointer" : "";

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
