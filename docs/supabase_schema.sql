-- =====================================================================
-- VerifyAI Supabase PostgreSQL Schema Migration
-- Run this in your Supabase SQL Editor:
-- https://supabase.com/dashboard/project/ejchzurnyvzhqcsqmbrl/sql/new
-- =====================================================================

-- 1. Events Table
CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    min_age INTEGER DEFAULT 18,
    max_age INTEGER,
    student_only BOOLEAN DEFAULT FALSE,
    allowed_id_types JSONB DEFAULT '["aadhaar", "pan", "college_id", "voter_id"]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Registrations Table
CREATE TABLE IF NOT EXISTS registrations (
    id TEXT PRIMARY KEY,
    event_id TEXT REFERENCES events(id) ON DELETE CASCADE,
    form_name TEXT NOT NULL,
    form_email TEXT,
    form_dob TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Verifications Table
CREATE TABLE IF NOT EXISTS verifications (
    id TEXT PRIMARY KEY,
    registration_id TEXT NOT NULL REFERENCES registrations(id) ON DELETE CASCADE,
    decision TEXT CHECK (decision IN ('approved', 'manual_review', 'rejected')),
    confidence NUMERIC(4, 2),
    reason TEXT,
    flags JSONB DEFAULT '[]'::jsonb,
    breakdown JSONB DEFAULT '{}'::jsonb,
    extracted_name TEXT,
    extracted_dob TEXT,
    extracted_id_number_masked TEXT,
    extracted_id_type TEXT,
    face_match_score NUMERIC(4, 3),
    name_match_score NUMERIC(5, 2),
    quality_score NUMERIC(4, 2),
    tampering_score NUMERIC(4, 3),
    is_duplicate BOOLEAN DEFAULT FALSE,
    processed_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Secure ID Hashes Table (For Duplicate Detection)
CREATE TABLE IF NOT EXISTS id_hashes (
    hash TEXT PRIMARY KEY,
    id_type TEXT NOT NULL,
    id_number_masked TEXT NOT NULL,
    registrant_name TEXT NOT NULL,
    registration_id TEXT NOT NULL REFERENCES registrations(id) ON DELETE CASCADE,
    event_id TEXT REFERENCES events(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for instant duplicate search
CREATE INDEX IF NOT EXISTS idx_id_hashes_hash ON id_hashes(hash);

-- Enable public access for publishable anon key (or disable RLS for direct hackathon access)
ALTER TABLE events DISABLE ROW LEVEL SECURITY;
ALTER TABLE registrations DISABLE ROW LEVEL SECURITY;
ALTER TABLE verifications DISABLE ROW LEVEL SECURITY;
ALTER TABLE id_hashes DISABLE ROW LEVEL SECURITY;

-- Seed Default Event
INSERT INTO events (id, name, min_age, student_only, allowed_id_types)
VALUES ('hackathon-2026', 'AI Build Challenge Bengaluru 2026', 18, FALSE, '["aadhaar", "pan", "college_id", "voter_id"]'::jsonb)
ON CONFLICT (id) DO NOTHING;
