'use client';

import React, { useState, useRef } from 'react';
import { Paperclip, ArrowUp, Sparkles, Image as ImageIcon } from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';

export const PromptBar: React.FC = () => {
  const { setActiveTab, setCommandPaletteOpen } = useAppStore();
  const [inputVal, setInputVal] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputVal.trim()) return;

    if (inputVal.toLowerCase().includes('sandbox') || inputVal.toLowerCase().includes('judge') || inputVal.toLowerCase().includes('preset')) {
      setActiveTab('sandbox');
    } else if (inputVal.toLowerCase().includes('upload') || inputVal.toLowerCase().includes('verify')) {
      setActiveTab('portal');
    } else {
      setCommandPaletteOpen(true);
    }
    setInputVal('');
  };

  const handleFileSelect = () => {
    setActiveTab('portal');
  };

  return (
    <div className="sticky bottom-4 z-30 max-w-2xl mx-auto px-4 w-full select-none">
      <form 
        onSubmit={handleSubmit}
        className="relative flex items-center rounded-2xl bg-slate-900/90 border border-white/12 shadow-2xl backdrop-blur-xl p-1.5 transition-all focus-within:border-indigo-500/50 focus-within:ring-2 focus-within:ring-indigo-500/20"
      >
        {/* Hidden File Input */}
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleFileSelect} 
          className="hidden" 
          accept="image/*"
        />

        {/* Attachment Paperclip Button */}
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          aria-label="Upload document image"
          className="p-2.5 rounded-xl text-slate-400 hover:text-white hover:bg-white/5 transition-colors cursor-pointer"
        >
          <Paperclip className="w-4 h-4" />
        </button>

        {/* Input Text Field */}
        <input
          type="text"
          value={inputVal}
          onChange={(e) => setInputVal(e.target.value)}
          placeholder="Upload ID image or type command (e.g. 'sandbox', 'verify', 'review')..."
          className="flex-1 bg-transparent px-2 text-sm text-white placeholder:text-slate-500 focus:outline-none"
        />

        {/* Submit Arrow Up Button (Confluence style) */}
        <button
          type="submit"
          aria-label="Submit verification prompt"
          disabled={!inputVal.trim()}
          className={`p-2 rounded-xl transition-all cursor-pointer ${
            inputVal.trim()
              ? 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-md shadow-indigo-600/30'
              : 'text-slate-500 hover:text-slate-400 hover:bg-white/5'
          }`}
        >
          <ArrowUp className="w-4 h-4" />
        </button>
      </form>

      {/* Subtle Bottom Helper Caption */}
      <div className="flex items-center justify-between text-[11px] text-slate-500 px-2 mt-1.5">
        <span className="flex items-center gap-1">
          <Sparkles className="w-3 h-3 text-emerald-400" />
          <span>AI Biometric & Duplicate Fraud Engine Active</span>
        </span>
        <span>Press <kbd className="font-mono text-slate-400">⌘K</kbd> for commands</span>
      </div>
    </div>
  );
};
