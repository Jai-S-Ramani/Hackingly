import json
import os
from typing import Optional, List, Dict, Any
from app.config import config

_supabase_client = None
DB_PATH = None

def _is_sqlite() -> bool:
    global DB_PATH
    return DB_PATH is not None or os.getenv("DATABASE_PROVIDER") == "sqlite" or config.get("database", {}).get("provider") == "sqlite"

def _get_sqlite_conn():
    global DB_PATH
    import sqlite3
    path = DB_PATH or config.get("database", {}).get("db_path") or "data/verifyai.db"
    os.makedirs(os.path.dirname(os.path.abspath(str(path))), exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn

def get_supabase_client():
    """Initializes and returns the authoritative Supabase client."""
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    db_cfg = config.get("database", {})
    url = db_cfg.get("supabase_url") or os.getenv("SUPABASE_URL")
    key = db_cfg.get("supabase_key") or os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError("Supabase configuration missing. Ensure SUPABASE_URL and SUPABASE_KEY are set.")

    from supabase import create_client
    _supabase_client = create_client(url, key)
    return _supabase_client

def is_supabase_active() -> bool:
    """Tests if Supabase is reachable and the required tables exist."""
    if _is_sqlite():
        return False
    try:
        client = get_supabase_client()
        client.table("events").select("id").limit(1).execute()
        return True
    except Exception:
        return False

def init_db():
    """Validates Supabase connection on startup, or initializes SQLite for test harnesses."""
    if _is_sqlite():
        conn = _get_sqlite_conn()
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                min_age INTEGER DEFAULT 18,
                student_only BOOLEAN DEFAULT 0,
                allowed_id_types TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                id TEXT PRIMARY KEY,
                event_id TEXT,
                form_name TEXT,
                form_email TEXT,
                form_dob TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS verifications (
                id TEXT PRIMARY KEY,
                registration_id TEXT,
                decision TEXT,
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
                is_duplicate BOOLEAN,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS id_hashes (
                id TEXT PRIMARY KEY,
                hash TEXT NOT NULL,
                id_type TEXT NOT NULL,
                id_number_masked TEXT NOT NULL,
                registrant_name TEXT NOT NULL,
                registration_id TEXT NOT NULL,
                event_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        return

    client = get_supabase_client()
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
            print("[INFO] Seeded default event 'hackathon-2026' into Supabase.")
    except Exception as e:
        print(f"[WARN] Failed to verify/seed default event in Supabase: {e}")

def save_registration_and_verification(
    reg_id: str,
    event_id: str,
    form_name: str,
    form_email: Optional[str],
    form_dob: Optional[str],
    verification_data: Dict[str, Any]
):
    """Saves registration and verification records directly to Supabase."""
    client = get_supabase_client()

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

def get_all_registrations(event_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetches all registrations with their verification status from Supabase."""
    client = get_supabase_client()
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

        flags = v.get("flags", [])
        if isinstance(flags, str):
            try:
                flags = json.loads(flags)
            except Exception:
                flags = [flags]

        breakdown = v.get("breakdown", {})
        if isinstance(breakdown, str):
            try:
                breakdown = json.loads(breakdown)
            except Exception:
                breakdown = {}

        formatted.append({
            "id": r.get("id"),
            "registration_id": r.get("id"),
            "event_id": r.get("event_id"),
            "form_name": r.get("form_name"),
            "form_email": r.get("form_email"),
            "form_dob": r.get("form_dob"),
            "created_at": r.get("created_at"),
            "decision": v.get("decision"),
            "confidence": float(v["confidence"]) if v.get("confidence") is not None else None,
            "reason": v.get("reason"),
            "flags": flags,
            "breakdown": breakdown,
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

def get_registration_by_id(reg_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves single registration and verification record from Supabase."""
    client = get_supabase_client()
    res = client.table("registrations").select("*, verifications(*)").eq("id", reg_id).execute()
    if not res.data:
        return None

    r = res.data[0]
    ver = r.get("verifications")
    v = ver[0] if isinstance(ver, list) and ver else (ver if isinstance(ver, dict) else {})

    flags = v.get("flags", [])
    if isinstance(flags, str):
        try:
            flags = json.loads(flags)
        except Exception:
            flags = [flags]

    breakdown = v.get("breakdown", {})
    if isinstance(breakdown, str):
        try:
            breakdown = json.loads(breakdown)
        except Exception:
            breakdown = {}

    return {
        "id": r.get("id"),
        "registration_id": r.get("id"),
        "event_id": r.get("event_id"),
        "form_name": r.get("form_name"),
        "form_email": r.get("form_email"),
        "form_dob": r.get("form_dob"),
        "created_at": r.get("created_at"),
        "decision": v.get("decision"),
        "confidence": float(v["confidence"]) if v.get("confidence") is not None else None,
        "reason": v.get("reason"),
        "flags": flags,
        "breakdown": breakdown,
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

def update_decision_override(reg_id: str, new_decision: str, reason: str):
    """Allows organizers to manually approve/reject a registration in Supabase."""
    client = get_supabase_client()
    client.table("verifications").update({
        "decision": new_decision,
        "reason": reason
    }).eq("registration_id", reg_id).execute()

def lookup_id_hashes(id_hash: str) -> List[Dict[str, Any]]:
    """Looks up existing registrations matching an ID SHA-256 fingerprint."""
    if _is_sqlite():
        conn = _get_sqlite_conn()
        c = conn.cursor()
        c.execute("SELECT registrant_name, registration_id, event_id, created_at FROM id_hashes WHERE hash = ?", (id_hash,))
        rows = [dict(row) for row in c.fetchall()]
        conn.close()
        return rows

    client = get_supabase_client()
    res = client.table("id_hashes").select("registrant_name, registration_id, event_id, created_at").eq("hash", id_hash).execute()
    return res.data or []

def register_id_hash(id_hash: str, id_type: str, id_number_masked: str, registrant_name: str, registration_id: str, event_id: Optional[str] = None):
    """Registers a new ID SHA-256 fingerprint."""
    if _is_sqlite():
        import uuid
        conn = _get_sqlite_conn()
        c = conn.cursor()
        c.execute(
            "INSERT INTO id_hashes (id, hash, id_type, id_number_masked, registrant_name, registration_id, event_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (f"hash_{uuid.uuid4().hex[:8]}", id_hash, id_type, id_number_masked, registrant_name, registration_id, event_id)
        )
        conn.commit()
        conn.close()
        return

    client = get_supabase_client()

    # Ensure parent registration exists to satisfy foreign key reference
    client.table("registrations").upsert({
        "id": registration_id,
        "form_name": registrant_name,
        "event_id": event_id or "hackathon-2026"
    }).execute()

    client.table("id_hashes").upsert({
        "hash": id_hash,
        "id_type": id_type,
        "id_number_masked": id_number_masked,
        "registrant_name": registrant_name,
        "registration_id": registration_id,
        "event_id": event_id
    }).execute()

def get_event_by_id(event_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves event configuration from Supabase."""
    client = get_supabase_client()
    res = client.table("events").select("*").eq("id", event_id).execute()
    if not res.data:
        return None
    return res.data[0]

def get_events() -> List[Dict[str, Any]]:
    """Retrieves all events from Supabase."""
    client = get_supabase_client()
    res = client.table("events").select("*").execute()
    return res.data or []
