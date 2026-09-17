import sqlite3
import json
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.config import config

DB_PATH = Path(config["database"]["db_path"])
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

_supabase_client = None

def get_supabase_client():
    """Initializes and returns the Supabase client if configured."""
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    db_cfg = config.get("database", {})
    provider = db_cfg.get("provider", "sqlite")
    url = db_cfg.get("supabase_url") or os.getenv("SUPABASE_URL")
    key = db_cfg.get("supabase_key") or os.getenv("SUPABASE_KEY")

    if provider == "supabase" and url and key:
        try:
            from supabase import create_client
            _supabase_client = create_client(url, key)
            return _supabase_client
        except Exception as e:
            print(f"[WARN] Failed to initialize Supabase client: {e}. Falling back to SQLite.")
            return None
    return None

def is_supabase_active() -> bool:
    """Tests if Supabase is reachable and the required tables exist."""
    client = get_supabase_client()
    if not client:
        return False
    try:
        # Quick ping on events table
        client.table("events").select("id").limit(1).execute()
        return True
    except Exception:
        return False

def get_connection() -> sqlite3.Connection:
    """Local SQLite connection."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes both SQLite schema and ensures events exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Events table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        min_age INTEGER DEFAULT 18,
        max_age INTEGER,
        student_only BOOLEAN DEFAULT 0,
        allowed_id_types TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Registrations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id TEXT PRIMARY KEY,
        event_id TEXT,
        form_name TEXT NOT NULL,
        form_email TEXT,
        form_dob TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(event_id) REFERENCES events(id)
    );
    """)

    # Verifications results table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS verifications (
        id TEXT PRIMARY KEY,
        registration_id TEXT NOT NULL,
        decision TEXT CHECK(decision IN ('approved', 'manual_review', 'rejected')),
        confidence REAL,
        reason TEXT,
        flags TEXT,
        breakdown TEXT,
        extracted_name TEXT,
        extracted_dob TEXT,
        extracted_id_number_masked TEXT,
        extracted_id_type TEXT,
        face_match_score REAL,
        name_match_score REAL,
        quality_score REAL,
        tampering_score REAL,
        is_duplicate BOOLEAN DEFAULT 0,
        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(registration_id) REFERENCES registrations(id)
    );
    """)

    # ID hashes registry table (for duplicate prevention)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS id_hashes (
        hash TEXT PRIMARY KEY,
        id_type TEXT NOT NULL,
        id_number_masked TEXT NOT NULL,
        registrant_name TEXT NOT NULL,
        registration_id TEXT NOT NULL,
        event_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Seed default event in SQLite
    cursor.execute("SELECT COUNT(*) as count FROM events WHERE id = 'hackathon-2026';")
    if cursor.fetchone()["count"] == 0:
        cursor.execute("""
        INSERT INTO events (id, name, min_age, student_only, allowed_id_types)
        VALUES (?, ?, ?, ?, ?);
        """, (
            "hackathon-2026",
            "AI Build Challenge Bengaluru 2026",
            18,
            0,
            json.dumps(["aadhaar", "pan", "college_id", "voter_id"])
        ))

    conn.commit()
    conn.close()

    # If Supabase is active, ensure default event exists there too
    client = get_supabase_client()
    if client:
        try:
            res = client.table("events").select("id").eq("id", "hackathon-2026").execute()
            if not res.data:
                client.table("events").insert({
                    "id": "hackathon-2026",
                    "name": "AI Build Challenge Bengaluru 2026",
                    "min_age": 18,
                    "student_only": False,
                    "allowed_id_types": ["aadhaar", "pan", "college_id", "voter_id"]
                }).execute()
        except Exception:
            pass

def save_registration_and_verification(
    reg_id: str,
    event_id: str,
    form_name: str,
    form_email: Optional[str],
    form_dob: Optional[str],
    verification_data: Dict[str, Any]
):
    """Saves registration and verification records to active database (Supabase and/or SQLite)."""
    # 1. Try saving to Supabase if active
    client = get_supabase_client()
    supabase_saved = False
    if client:
        try:
            client.table("registrations").upsert({
                "id": reg_id,
                "event_id": event_id,
                "form_name": form_name,
                "form_email": form_email,
                "form_dob": form_dob
            }).execute()

            client.table("verifications").upsert({
                "id": verification_data.get("verification_id", f"ver_{reg_id}"),
                "registration_id": reg_id,
                "decision": verification_data.get("decision"),
                "confidence": verification_data.get("confidence"),
                "reason": verification_data.get("reason"),
                "flags": verification_data.get("flags", []),
                "breakdown": verification_data.get("breakdown", {}),
                "extracted_name": verification_data.get("extracted_name"),
                "extracted_dob": verification_data.get("extracted_dob"),
                "extracted_id_number_masked": verification_data.get("extracted_id_number_masked"),
                "extracted_id_type": verification_data.get("extracted_id_type"),
                "face_match_score": verification_data.get("face_match_score"),
                "name_match_score": verification_data.get("name_match_score"),
                "quality_score": verification_data.get("quality_score"),
                "tampering_score": verification_data.get("tampering_score"),
                "is_duplicate": bool(verification_data.get("is_duplicate"))
            }).execute()
            supabase_saved = True
        except Exception as e:
            print(f"[WARN] Supabase save failed: {e}. Falling back to SQLite.")

    # 2. Always maintain SQLite record as resilient backup / local store
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO registrations (id, event_id, form_name, form_email, form_dob)
    VALUES (?, ?, ?, ?, ?);
    """, (reg_id, event_id, form_name, form_email, form_dob))

    cursor.execute("""
    INSERT OR REPLACE INTO verifications (
        id, registration_id, decision, confidence, reason, flags, breakdown,
        extracted_name, extracted_dob, extracted_id_number_masked, extracted_id_type,
        face_match_score, name_match_score, quality_score, tampering_score, is_duplicate
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        verification_data.get("verification_id", f"ver_{reg_id}"),
        reg_id,
        verification_data.get("decision"),
        verification_data.get("confidence"),
        verification_data.get("reason"),
        json.dumps(verification_data.get("flags", [])),
        json.dumps(verification_data.get("breakdown", {})),
        verification_data.get("extracted_name"),
        verification_data.get("extracted_dob"),
        verification_data.get("extracted_id_number_masked"),
        verification_data.get("extracted_id_type"),
        verification_data.get("face_match_score"),
        verification_data.get("name_match_score"),
        verification_data.get("quality_score"),
        verification_data.get("tampering_score"),
        1 if verification_data.get("is_duplicate") else 0
    ))

    conn.commit()
    conn.close()

def get_all_registrations(event_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetches all registrations with their verification status from Supabase (or SQLite)."""
    client = get_supabase_client()
    if client:
        try:
            query = client.table("registrations").select("*, verifications(*)")
            if event_id:
                query = query.eq("event_id", event_id)
            res = query.order("created_at", desc=True).execute()

            formatted = []
            for r in res.data or []:
                ver = r.get("verifications")
                if isinstance(ver, list) and ver:
                    v = ver[0]
                elif isinstance(ver, dict):
                    v = ver
                else:
                    v = {}

                # Filter by status if specified
                if status and status != "all" and v.get("decision") != status:
                    continue

                formatted.append({
                    "registration_id": r.get("id"),
                    "event_id": r.get("event_id"),
                    "form_name": r.get("form_name"),
                    "form_email": r.get("form_email"),
                    "form_dob": r.get("form_dob"),
                    "created_at": r.get("created_at"),
                    "decision": v.get("decision"),
                    "confidence": float(v["confidence"]) if v.get("confidence") is not None else None,
                    "reason": v.get("reason"),
                    "flags": v.get("flags", []) if isinstance(v.get("flags"), list) else [],
                    "breakdown": v.get("breakdown", {}) if isinstance(v.get("breakdown"), dict) else {},
                    "extracted_name": v.get("extracted_name"),
                    "extracted_dob": v.get("extracted_dob"),
                    "extracted_id_number_masked": v.get("extracted_id_number_masked"),
                    "extracted_id_type": v.get("extracted_id_type"),
                    "face_match_score": float(v["face_match_score"]) if v.get("face_match_score") is not None else None,
                    "name_match_score": float(v["name_match_score"]) if v.get("name_match_score") is not None else None,
                    "quality_score": float(v["quality_score"]) if v.get("quality_score") is not None else None,
                    "tampering_score": float(v["tampering_score"]) if v.get("tampering_score") is not None else None,
                    "is_duplicate": bool(v.get("is_duplicate")),
                    "processed_at": v.get("processed_at")
                })
            return formatted
        except Exception as e:
            # Fallback to SQLite
            pass

    # SQLite query
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        r.id as registration_id,
        r.event_id,
        r.form_name,
        r.form_email,
        r.form_dob,
        r.created_at,
        v.decision,
        v.confidence,
        v.reason,
        v.flags,
        v.breakdown,
        v.extracted_name,
        v.extracted_dob,
        v.extracted_id_number_masked,
        v.extracted_id_type,
        v.face_match_score,
        v.name_match_score,
        v.quality_score,
        v.tampering_score,
        v.is_duplicate,
        v.processed_at
    FROM registrations r
    LEFT JOIN verifications v ON r.id = v.registration_id
    WHERE 1=1
    """
    params = []
    if event_id:
        query += " AND r.event_id = ?"
        params.append(event_id)
    if status and status != "all":
        query += " AND v.decision = ?"
        params.append(status)

    query += " ORDER BY v.processed_at DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    results = []
    for r in rows:
        d = dict(r)
        if d.get("flags"):
            try:
                d["flags"] = json.loads(d["flags"])
            except Exception:
                d["flags"] = []
        if d.get("breakdown"):
            try:
                d["breakdown"] = json.loads(d["breakdown"])
            except Exception:
                d["breakdown"] = {}
        results.append(d)

    conn.close()
    return results

def get_registration_by_id(reg_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves single registration and verification record."""
    client = get_supabase_client()
    if client:
        try:
            res = client.table("registrations").select("*, verifications(*)").eq("id", reg_id).execute()
            if res.data:
                r = res.data[0]
                ver = r.get("verifications")
                v = ver[0] if isinstance(ver, list) and ver else (ver if isinstance(ver, dict) else {})
                return {
                    "registration_id": r.get("id"),
                    "event_id": r.get("event_id"),
                    "form_name": r.get("form_name"),
                    "form_email": r.get("form_email"),
                    "form_dob": r.get("form_dob"),
                    "created_at": r.get("created_at"),
                    "decision": v.get("decision"),
                    "confidence": float(v["confidence"]) if v.get("confidence") is not None else None,
                    "reason": v.get("reason"),
                    "flags": v.get("flags", []) if isinstance(v.get("flags"), list) else [],
                    "breakdown": v.get("breakdown", {}) if isinstance(v.get("breakdown"), dict) else {},
                    "extracted_name": v.get("extracted_name"),
                    "extracted_dob": v.get("extracted_dob"),
                    "extracted_id_number_masked": v.get("extracted_id_number_masked"),
                    "extracted_id_type": v.get("extracted_id_type"),
                    "face_match_score": float(v["face_match_score"]) if v.get("face_match_score") is not None else None,
                    "name_match_score": float(v["name_match_score"]) if v.get("name_match_score") is not None else None,
                    "quality_score": float(v["quality_score"]) if v.get("quality_score") is not None else None,
                    "tampering_score": float(v["tampering_score"]) if v.get("tampering_score") is not None else None,
                    "is_duplicate": bool(v.get("is_duplicate")),
                    "processed_at": v.get("processed_at")
                }
        except Exception:
            pass

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        r.id as registration_id,
        r.event_id,
        r.form_name,
        r.form_email,
        r.form_dob,
        r.created_at,
        v.decision,
        v.confidence,
        v.reason,
        v.flags,
        v.breakdown,
        v.extracted_name,
        v.extracted_dob,
        v.extracted_id_number_masked,
        v.extracted_id_type,
        v.face_match_score,
        v.name_match_score,
        v.quality_score,
        v.tampering_score,
        v.is_duplicate,
        v.processed_at
    FROM registrations r
    LEFT JOIN verifications v ON r.id = v.registration_id
    WHERE r.id = ?;
    """, (reg_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    if d.get("flags"):
        try:
            d["flags"] = json.loads(d["flags"])
        except Exception:
            d["flags"] = []
    if d.get("breakdown"):
        try:
            d["breakdown"] = json.loads(d["breakdown"])
        except Exception:
            d["breakdown"] = {}
    return d

def update_decision_override(reg_id: str, new_decision: str, reason: str):
    """Allows organizers to manually approve/reject a registration."""
    client = get_supabase_client()
    if client:
        try:
            client.table("verifications").update({
                "decision": new_decision,
                "reason": reason
            }).eq("registration_id", reg_id).execute()
        except Exception:
            pass

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE verifications 
    SET decision = ?, reason = ?
    WHERE registration_id = ?;
    """, (new_decision, reason, reg_id))
    conn.commit()
    conn.close()

def lookup_id_hashes(id_hash: str) -> List[Dict[str, Any]]:
    """Looks up existing registrations matching an ID SHA-256 fingerprint."""
    client = get_supabase_client()
    if client:
        try:
            res = client.table("id_hashes").select("registrant_name, registration_id, event_id, created_at").eq("hash", id_hash).execute()
            if res.data is not None:
                return res.data
        except Exception:
            pass

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT registrant_name, registration_id, event_id, created_at
    FROM id_hashes
    WHERE hash = ?;
    """, (id_hash,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def register_id_hash(id_hash: str, id_type: str, id_number_masked: str, registrant_name: str, registration_id: str, event_id: Optional[str] = None):
    """Registers a new ID SHA-256 fingerprint in the database."""
    client = get_supabase_client()
    if client:
        try:
            client.table("id_hashes").upsert({
                "hash": id_hash,
                "id_type": id_type,
                "id_number_masked": id_number_masked,
                "registrant_name": registrant_name,
                "registration_id": registration_id,
                "event_id": event_id
            }).execute()
        except Exception:
            pass

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO id_hashes (hash, id_type, id_number_masked, registrant_name, registration_id, event_id)
    VALUES (?, ?, ?, ?, ?, ?);
    """, (id_hash, id_type, id_number_masked, registrant_name, registration_id, event_id))
    conn.commit()
    conn.close()
