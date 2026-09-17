import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://ejchzurnyvzhqcsqmbrl.supabase.co';
const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'sb_publishable_Gpbr08o4g-iXHyqHTxumlg_uX0HfV5L';

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
