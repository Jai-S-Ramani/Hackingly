"""
Seeds clean, diverse, realistic hackathon demo data into data/verifyai.db
Covers comprehensive real-world scenarios:
- Genuine Aadhaar, PAN, College ID, Voter ID (Auto-Approved)
- Duplicate ID Fraud: Reused under different name (Rejected)
- User Already Entered: Double submission by same registrant (Rejected)
- Underage Participant: < 18 years old (Rejected)
- Digital Tampering: ELA and compression artifact flag (Rejected)
- Biometric Face Mismatch: Selfie does not match ID photo (Rejected)
- Severe Name Mismatch: Submitted name differs completely from ID (Rejected)
- Low Clarity / Blurry scan (Manual Review)
- Name abbreviation / discrepancy (Manual Review)
- Partial OCR Occlusion (Manual Review)
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import sqlite3
import json
import uuid
import hashlib
from datetime import datetime, timedelta

DB_PATH = "data/verifyai.db"

def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop existing demo data and recreate clean schema
    cursor.execute("DROP TABLE IF EXISTS verifications;")
    cursor.execute("DROP TABLE IF EXISTS registrations;")
    cursor.execute("DROP TABLE IF EXISTS id_hashes;")
    cursor.execute("DROP TABLE IF EXISTS events;")

    cursor.execute("""
    CREATE TABLE events (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        min_age INTEGER DEFAULT 18,
        max_age INTEGER,
        student_only BOOLEAN DEFAULT 0,
        allowed_id_types TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE registrations (
        id TEXT PRIMARY KEY,
        event_id TEXT,
        form_name TEXT NOT NULL,
        form_email TEXT,
        form_dob TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(event_id) REFERENCES events(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE verifications (
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

    cursor.execute("""
    CREATE TABLE id_hashes (
        hash TEXT PRIMARY KEY,
        id_type TEXT NOT NULL,
        id_number_masked TEXT NOT NULL,
        registrant_name TEXT NOT NULL,
        registration_id TEXT NOT NULL,
        event_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Seed Default Event
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

    # Comprehensive Brand New Demo Datasets
    records = [
        # --- 1. Genuine Approvals ---
        {
            "reg_id": "reg_101",
            "name": "Arjun Kumar",
            "email": "arjun.kumar@gmail.com",
            "dob": "1998-05-14",
            "extracted_name": "ARJUN KUMAR",
            "id_type": "aadhaar",
            "id_num_clean": "234567890124",
            "id_masked": "****0124",
            "decision": "approved",
            "confidence": 0.95,
            "reason": "All checks passed successfully. Identity and eligibility verified with high confidence.",
            "flags": [],
            "face_score": 0.94,
            "name_score": 98.0,
            "quality_score": 0.96,
            "tampering_score": 0.03,
            "is_dup": False,
            "min_ago": 60
        },
        {
            "reg_id": "reg_102",
            "name": "Priya Sharma",
            "email": "priya.sharma@outlook.com",
            "dob": "2001-08-22",
            "extracted_name": "PRIYA SHARMA",
            "id_type": "pan",
            "id_num_clean": "ABCPS8492K",
            "id_masked": "****8492K",
            "decision": "approved",
            "confidence": 0.93,
            "reason": "All checks passed successfully. PAN identity verified with high confidence.",
            "flags": [],
            "face_score": 0.91,
            "name_score": 97.0,
            "quality_score": 0.94,
            "tampering_score": 0.04,
            "is_dup": False,
            "min_ago": 52
        },
        {
            "reg_id": "reg_103",
            "name": "Rahul Verma",
            "email": "rahul.v@iitd.ac.in",
            "dob": "2002-11-03",
            "extracted_name": "RAHUL VERMA",
            "id_type": "college_id",
            "id_num_clean": "2021CS10452",
            "id_masked": "****0452",
            "decision": "approved",
            "confidence": 0.91,
            "reason": "Student identity verified. Validated College ID from Indian Institute of Technology.",
            "flags": [],
            "face_score": 0.88,
            "name_score": 95.0,
            "quality_score": 0.92,
            "tampering_score": 0.05,
            "is_dup": False,
            "min_ago": 45
        },
        {
            "reg_id": "reg_104",
            "name": "Ananya Iyer",
            "email": "ananya.iyer@bits-pilani.ac.in",
            "dob": "2003-02-17",
            "extracted_name": "ANANYA IYER",
            "id_type": "college_id",
            "id_num_clean": "2022A7PS0192P",
            "id_masked": "****0192P",
            "decision": "approved",
            "confidence": 0.94,
            "reason": "Student registration verified with high confidence.",
            "flags": [],
            "face_score": 0.92,
            "name_score": 98.0,
            "quality_score": 0.95,
            "tampering_score": 0.02,
            "is_dup": False,
            "min_ago": 40
        },
        {
            "reg_id": "reg_105",
            "name": "Kavita Patel",
            "email": "kavita.patel@gmail.com",
            "dob": "1999-07-30",
            "extracted_name": "KAVITA PATEL",
            "id_type": "voter_id",
            "id_num_clean": "WKP4928174",
            "id_masked": "****8174",
            "decision": "approved",
            "confidence": 0.89,
            "reason": "Voter ID identity verified. Clean biometric and demographic match.",
            "flags": [],
            "face_score": 0.87,
            "name_score": 94.0,
            "quality_score": 0.90,
            "tampering_score": 0.04,
            "is_dup": False,
            "min_ago": 35
        },
        {
            "reg_id": "reg_106",
            "name": "Nikhil Nair",
            "email": "nikhil.nair@techcorp.in",
            "dob": "1997-01-15",
            "extracted_name": "NIKHIL NAIR",
            "id_type": "aadhaar",
            "id_num_clean": "849201948271",
            "id_masked": "****8271",
            "decision": "approved",
            "confidence": 0.92,
            "reason": "All checks passed successfully. Identity verified with high confidence.",
            "flags": [],
            "face_score": 0.90,
            "name_score": 96.0,
            "quality_score": 0.93,
            "tampering_score": 0.03,
            "is_dup": False,
            "min_ago": 30
        },
        {
            "reg_id": "reg_107",
            "name": "Sneha Kulkarni",
            "email": "sneha.kulkarni@devmail.org",
            "dob": "2000-04-12",
            "extracted_name": "SNEHA KULKARNI",
            "id_type": "pan",
            "id_num_clean": "KLKPS9182R",
            "id_masked": "****9182R",
            "decision": "approved",
            "confidence": 0.90,
            "reason": "Identity verified with PAN card match.",
            "flags": [],
            "face_score": 0.86,
            "name_score": 95.0,
            "quality_score": 0.91,
            "tampering_score": 0.04,
            "is_dup": False,
            "min_ago": 26
        },
        {
            "reg_id": "reg_108",
            "name": "Tanmay Joshi",
            "email": "tanmay.j@nitt.edu",
            "dob": "2003-09-08",
            "extracted_name": "TANMAY JOSHI",
            "id_type": "college_id",
            "id_num_clean": "106121089",
            "id_masked": "****1089",
            "decision": "approved",
            "confidence": 0.88,
            "reason": "Verified College ID from National Institute of Technology Trichy.",
            "flags": [],
            "face_score": 0.84,
            "name_score": 93.0,
            "quality_score": 0.89,
            "tampering_score": 0.06,
            "is_dup": False,
            "min_ago": 22
        },

        # --- 2. Fraud & Violations (Rejected) ---
        {
            "reg_id": "reg_109",
            "name": "Vikram Singh",
            "email": "vikram.singh@fraud.net",
            "dob": "1998-05-14",
            "extracted_name": "ARJUN KUMAR",
            "id_type": "aadhaar",
            "id_num_clean": "234567890124", # Reusing Arjun's Aadhaar!
            "id_masked": "****0124",
            "decision": "rejected",
            "confidence": 0.38,
            "reason": "Duplicate ID detected: This document was already registered by another participant (Arjun Kumar).",
            "flags": ["name_mismatch", "duplicate_id_different_name"],
            "face_score": 0.35,
            "name_score": 25.0,
            "quality_score": 0.91,
            "tampering_score": 0.04,
            "is_dup": True,
            "min_ago": 18
        },
        {
            "reg_id": "reg_110",
            "name": "Arjun Kumar",
            "email": "arjun.kumar@gmail.com",
            "dob": "1998-05-14",
            "extracted_name": "ARJUN KUMAR",
            "id_type": "aadhaar",
            "id_num_clean": "234567890124", # Double entry attempt
            "id_masked": "****0124",
            "decision": "rejected",
            "confidence": 0.48,
            "reason": "User Already Entered: A registration with this identification document has already been submitted for this event.",
            "flags": ["user_already_registered"],
            "face_score": 0.94,
            "name_score": 98.0,
            "quality_score": 0.96,
            "tampering_score": 0.03,
            "is_dup": True,
            "min_ago": 15
        },
        {
            "reg_id": "reg_111",
            "name": "Rohan Das",
            "email": "rohan.das16@gmail.com",
            "dob": "2010-09-12",
            "extracted_name": "ROHAN DAS",
            "id_type": "aadhaar",
            "id_num_clean": "782940182741",
            "id_masked": "****2741",
            "decision": "rejected",
            "confidence": 0.45,
            "reason": "Age restriction failure: Participant is 16 years old (minimum 18+ required for hackathon entry).",
            "flags": ["underage_participant_16_years"],
            "face_score": 0.85,
            "name_score": 95.0,
            "quality_score": 0.90,
            "tampering_score": 0.04,
            "is_dup": False,
            "min_ago": 12
        },
        {
            "reg_id": "reg_112",
            "name": "Devendra Mehta",
            "email": "devendra.m@yahoo.com",
            "dob": "1995-04-19",
            "extracted_name": "DEVENDRA MEHTA",
            "id_type": "aadhaar",
            "id_num_clean": "492019482910",
            "id_masked": "****2910",
            "decision": "rejected",
            "confidence": 0.32,
            "reason": "Document tampering detected: Image exhibits digital modification and high Error Level Analysis (ELA) variance.",
            "flags": ["potential_tampering_ela", "editing_software_photoshop"],
            "face_score": 0.78,
            "name_score": 88.0,
            "quality_score": 0.42,
            "tampering_score": 0.82,
            "is_dup": False,
            "min_ago": 10
        },
        {
            "reg_id": "reg_113",
            "name": "Sameer Khan",
            "email": "sameer.khan@domain.com",
            "dob": "1999-10-18",
            "extracted_name": "SAMEER KHAN",
            "id_type": "aadhaar",
            "id_num_clean": "582910492810",
            "id_masked": "****2810",
            "decision": "rejected",
            "confidence": 0.40,
            "reason": "Biometric face verification failure: Participant selfie does not match the portrait extracted from the ID document.",
            "flags": ["face_mismatch"],
            "face_score": 0.22,
            "name_score": 96.0,
            "quality_score": 0.92,
            "tampering_score": 0.04,
            "is_dup": False,
            "min_ago": 8
        },
        {
            "reg_id": "reg_114",
            "name": "Siddharth Jain",
            "email": "sid.jain99@gmail.com",
            "dob": "1999-06-25",
            "extracted_name": "RAJESH GUPTA",
            "id_type": "pan",
            "id_num_clean": "GUPTR4819M",
            "id_masked": "****4819M",
            "decision": "rejected",
            "confidence": 0.36,
            "reason": "Identity mismatch: Form registrant name differs completely from document name ('RAJESH GUPTA').",
            "flags": ["name_mismatch"],
            "face_score": 0.45,
            "name_score": 18.0,
            "quality_score": 0.93,
            "tampering_score": 0.05,
            "is_dup": False,
            "min_ago": 6
        },

        # --- 3. Manual Review Scenarios ---
        {
            "reg_id": "reg_115",
            "name": "Sunita Rao",
            "email": "sunita.rao@hotmail.com",
            "dob": "2000-12-05",
            "extracted_name": "SUNITA RAO",
            "id_type": "pan",
            "id_num_clean": "SRAPN2910M",
            "id_masked": "****2910M",
            "decision": "manual_review",
            "confidence": 0.56,
            "reason": "Borderline confidence (56%): Routed for manual review due to low image clarity / motion blur.",
            "flags": ["blurry_image"],
            "face_score": 0.65,
            "name_score": 85.0,
            "quality_score": 0.48,
            "tampering_score": 0.07,
            "is_dup": False,
            "min_ago": 4
        },
        {
            "reg_id": "reg_116",
            "name": "Amit Roy", # Abbreviated form name vs "AMITABH ROY"
            "email": "amit.roy@tech.org",
            "dob": "1997-03-24",
            "extracted_name": "AMITABH ROY",
            "id_type": "pan",
            "id_num_clean": "AMTPN9182L",
            "id_masked": "****9182L",
            "decision": "manual_review",
            "confidence": 0.68,
            "reason": "Borderline confidence (68%): Routed for manual review due to slight name discrepancy.",
            "flags": ["name_partial_match"],
            "face_score": 0.85,
            "name_score": 72.0,
            "quality_score": 0.90,
            "tampering_score": 0.05,
            "is_dup": False,
            "min_ago": 2
        },
        {
            "reg_id": "reg_117",
            "name": "Neha Deshmukh",
            "email": "neha.desh@gmail.com",
            "dob": "2001-11-14",
            "extracted_name": "NEHA DESHMUKH",
            "id_type": "aadhaar",
            "id_num_clean": "392019482710",
            "id_masked": "****2710",
            "decision": "manual_review",
            "confidence": 0.63,
            "reason": "Borderline confidence (63%): Document corner partially shadowed, requires organizer verification.",
            "flags": ["borderline_ocr_confidence"],
            "face_score": 0.76,
            "name_score": 90.0,
            "quality_score": 0.72,
            "tampering_score": 0.08,
            "is_dup": False,
            "min_ago": 1
        }
    ]

    now = datetime.now()

    for item in records:
        time_stamp = (now - timedelta(minutes=item["min_ago"])).strftime("%Y-%m-%d %H:%M:%S")

        # Insert Registration
        cursor.execute("""
        INSERT INTO registrations (id, event_id, form_name, form_email, form_dob, created_at)
        VALUES (?, ?, ?, ?, ?, ?);
        """, (
            item["reg_id"],
            "hackathon-2026",
            item["name"],
            item["email"],
            item["dob"],
            time_stamp
        ))

        # Breakdown object
        breakdown = {
            "quality": {
                "score": item["quality_score"],
                "blur_score": 240.0 if "blurry_image" not in item["flags"] else 38.0,
                "tampering_score": item["tampering_score"],
                "resolution_ok": True,
                "detected_doc_type": item["id_type"]
            },
            "extraction": {
                "score": 0.90,
                "name": item["extracted_name"],
                "date_of_birth": item["dob"],
                "id_number_masked": item["id_masked"],
                "id_type": item["id_type"],
                "format_valid": True,
                "checksum_valid": True
            },
            "identity": {
                "face_match_score": item["face_score"],
                "face_match_verdict": "match" if item["face_score"] and item["face_score"] > 0.6 else "mismatch",
                "name_match_score": item["name_score"],
                "name_match_verdict": "match" if item["name_score"] >= 85 else ("uncertain" if item["name_score"] >= 65 else "mismatch")
            },
            "duplicate": {
                "is_duplicate": item["is_dup"],
                "details": item["reason"] if item["is_dup"] else "No duplicates found. First-time registration."
            },
            "eligibility": {
                "age_check": "fail" if "underage" in str(item["flags"]) else "pass",
                "student_check": "pass"
            }
        }

        # Insert Verification
        cursor.execute("""
        INSERT INTO verifications (
            id, registration_id, decision, confidence, reason, flags, breakdown,
            extracted_name, extracted_dob, extracted_id_number_masked, extracted_id_type,
            face_match_score, name_match_score, quality_score, tampering_score, is_duplicate, processed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            f"ver_{item['reg_id']}",
            item["reg_id"],
            item["decision"],
            item["confidence"],
            item["reason"],
            json.dumps(item["flags"]),
            json.dumps(breakdown),
            item["extracted_name"],
            item["dob"],
            item["id_masked"],
            item["id_type"],
            item["face_score"],
            item["name_score"],
            item["quality_score"],
            item["tampering_score"],
            1 if item["is_dup"] else 0,
            time_stamp
        ))

        # Only insert into id_hashes if not already in hashes
        id_hash = hashlib.sha256(f"{item['id_type']}:{item['id_num_clean']}".encode("utf-8")).hexdigest()
        cursor.execute("SELECT COUNT(*) FROM id_hashes WHERE hash = ?;", (id_hash,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
            INSERT INTO id_hashes (hash, id_type, id_number_masked, registrant_name, registration_id, event_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (
                id_hash,
                item["id_type"],
                item["id_masked"],
                item["name"],
                item["reg_id"],
                "hackathon-2026",
                time_stamp
            ))

    conn.commit()
    conn.close()

    # Seed into Supabase by default
    from app.database import get_supabase_client
    client = get_supabase_client()
    if not client:
        print("[WARN] Supabase client could not be initialized. Check SUPABASE_URL and SUPABASE_KEY in .env")
        return
    
    print("[INFO] Seeding demo registrations directly into Supabase Cloud...")
    try:
        # 1. Upsert Event
        client.table("events").upsert({
            "id": "hackathon-2026",
            "name": "AI Build Challenge Bengaluru 2026",
            "min_age": 18,
            "student_only": False,
            "allowed_id_types": ["aadhaar", "pan", "college_id", "voter_id"]
        }).execute()

        for item in records:
            time_stamp = (now - timedelta(minutes=item["min_ago"])).isoformat()
            
            # Registration
            client.table("registrations").upsert({
                "id": item["reg_id"],
                "event_id": "hackathon-2026",
                "form_name": item["name"],
                "form_email": item["email"],
                "form_dob": item["dob"]
            }).execute()

            # Breakdown
            bd = {
                "quality": {
                    "score": item["quality_score"],
                    "blur_score": 240.0 if "blurry_image" not in item["flags"] else 38.0,
                    "tampering_score": item["tampering_score"],
                    "resolution_ok": True,
                    "detected_doc_type": item["id_type"]
                },
                "extraction": {
                    "score": 0.90,
                    "name": item["extracted_name"],
                    "date_of_birth": item["dob"],
                    "id_number_masked": item["id_masked"],
                    "id_type": item["id_type"],
                    "format_valid": True,
                    "checksum_valid": True
                },
                "identity": {
                    "face_match_score": item["face_score"],
                    "face_match_verdict": "match" if item["face_score"] and item["face_score"] > 0.6 else "mismatch",
                    "name_match_score": item["name_score"],
                    "name_match_verdict": "match" if item["name_score"] >= 85 else ("uncertain" if item["name_score"] >= 65 else "mismatch")
                },
                "duplicate": {
                    "is_duplicate": item["is_dup"],
                    "details": item["reason"] if item["is_dup"] else "No duplicates found. First-time registration."
                },
                "eligibility": {
                    "age_check": "fail" if "underage" in str(item["flags"]) else "pass",
                    "student_check": "pass"
                }
            }

            # Verification
            client.table("verifications").upsert({
                "id": f"ver_{item['reg_id']}",
                "registration_id": item["reg_id"],
                "decision": item["decision"],
                "confidence": item["confidence"],
                "reason": item["reason"],
                "flags": item["flags"],
                "breakdown": bd,
                "extracted_name": item["extracted_name"],
                "extracted_dob": item["dob"],
                "extracted_id_number_masked": item["id_masked"],
                "extracted_id_type": item["id_type"],
                "face_match_score": item["face_score"],
                "name_match_score": item["name_score"],
                "quality_score": item["quality_score"],
                "tampering_score": item["tampering_score"],
                "is_duplicate": bool(item["is_dup"])
            }).execute()

            # ID Hash
            id_hash = hashlib.sha256(f"{item['id_type']}:{item['id_num_clean']}".encode("utf-8")).hexdigest()
            client.table("id_hashes").upsert({
                "hash": id_hash,
                "id_type": item["id_type"],
                "id_number_masked": item["id_masked"],
                "registrant_name": item["name"],
                "registration_id": item["reg_id"],
                "event_id": "hackathon-2026"
            }).execute()

        print(f"[SUCCESS] Successfully seeded {len(records)} registrations directly into Supabase cloud!")
    except Exception as e:
        print(f"[ERROR] Failed to seed into Supabase: {e}")
        print("Note: Ensure the SQL schema migration in docs/supabase_schema.sql has been executed in the Supabase Dashboard SQL Editor.")

if __name__ == "__main__":
    seed_database()
