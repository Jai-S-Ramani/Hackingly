import { ApiVerificationService } from './apiService';
import { IVerificationService } from './IVerificationService';

// Singleton instance
export const verificationService: IVerificationService = new ApiVerificationService();

export * from './types';
export * from './mockData';
export { supabase } from './supabaseService';
