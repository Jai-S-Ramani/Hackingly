import { create } from 'zustand';
import { Registration, TelemetryMetrics, JudgePreset } from '../services/types';
import { verificationService } from '../services';

export type ActiveTab = 'hub' | 'feed' | 'sandbox' | 'portal' | 'analytics';

interface AppState {
  activeTab: ActiveTab;
  setActiveTab: (tab: ActiveTab) => void;

  registrations: Registration[];
  isLoading: boolean;
  selectedRegistration: Registration | null;
  setSelectedRegistration: (reg: Registration | null) => void;

  statusFilter: string;
  setStatusFilter: (s: string) => void;

  searchQuery: string;
  setSearchQuery: (q: string) => void;

  commandPaletteOpen: boolean;
  setCommandPaletteOpen: (open: boolean) => void;

  mobileMenuOpen: boolean;
  setMobileMenuOpen: (open: boolean) => void;

  activePreset: JudgePreset | null;
  setActivePreset: (preset: JudgePreset | null) => void;

  pendingUploadFile: File | null;
  setPendingUploadFile: (file: File | null) => void;

  telemetry: TelemetryMetrics | null;
  fetchRegistrations: () => Promise<void>;
  fetchTelemetry: () => Promise<void>;
  updateReviewDecision: (id: string, decision: 'approved' | 'rejected', notes: string) => Promise<boolean>;
}

export const useAppStore = create<AppState>((set, get) => ({
  activeTab: 'hub',
  setActiveTab: (activeTab) => set({ activeTab, mobileMenuOpen: false }),

  registrations: [],
  isLoading: false,
  selectedRegistration: null,
  setSelectedRegistration: (selectedRegistration) => set({ selectedRegistration }),

  statusFilter: 'all',
  setStatusFilter: (statusFilter) => {
    set({ statusFilter });
    get().fetchRegistrations();
  },

  searchQuery: '',
  setSearchQuery: (searchQuery) => {
    set({ searchQuery });
    get().fetchRegistrations();
  },

  commandPaletteOpen: false,
  setCommandPaletteOpen: (commandPaletteOpen) => set({ commandPaletteOpen }),

  mobileMenuOpen: false,
  setMobileMenuOpen: (mobileMenuOpen) => set({ mobileMenuOpen }),

  activePreset: null,
  setActivePreset: (activePreset) => set({ activePreset }),

  pendingUploadFile: null,
  setPendingUploadFile: (pendingUploadFile) => set({ pendingUploadFile }),

  telemetry: null,

  fetchRegistrations: async () => {
    set({ isLoading: true });
    try {
      const data = await verificationService.getRegistrations({
        status: get().statusFilter,
        search: get().searchQuery
      });
      set({ registrations: data, isLoading: false });
    } catch (err) {
      console.error("fetchRegistrations error:", err);
      set({ isLoading: false });
    }
  },

  fetchTelemetry: async () => {
    try {
      const telemetry = await verificationService.getTelemetry();
      set({ telemetry });
    } catch (err) {
      console.error("fetchTelemetry error:", err);
    }
  },

  updateReviewDecision: async (id: string, decision: 'approved' | 'rejected', notes: string) => {
    const success = await verificationService.updateReviewDecision(id, decision, notes);
    if (success) {
      await get().fetchRegistrations();
      await get().fetchTelemetry();
      const currentSelected = get().selectedRegistration;
      if (currentSelected && currentSelected.id === id) {
        set({
          selectedRegistration: {
            ...currentSelected,
            decision,
            reasons: [...currentSelected.reasons, `Manual Review: ${notes}`]
          }
        });
      }
    }
    return success;
  }
}));
