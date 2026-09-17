import hashlib
import re
from typing import Dict, Any, Optional
from app.database import get_connection

class DuplicateDetector:
    def __init__(self):
        pass

    def check_and_register(
        self,
        id_type: Optional[str],
        id_number: Optional[str],
        registrant_name: str,
        registration_id: str,
        event_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Runs Stage 4 Duplicate Detection:
        1. Computes SHA-256 fingerprint of ID document.
        2. Queries database for previous registrations with same ID.
        3. If already registered:
           - Same name: Flags as 'user_already_registered' (prevents multiple entries)
           - Different name: Flags as 'duplicate_id_different_name' (impersonation fraud)
        """
        if not id_number or not id_type:
            return {
                "is_duplicate": False,
                "flags": [],
                "details": "ID number was not extracted; duplicate check skipped"
            }

        # Normalize ID number (remove spaces, uppercase)
        clean_id = re.sub(r"[\s\-_]", "", id_number).upper()
        clean_name = registrant_name.strip().lower()

        # SHA-256 fingerprint
        raw_fingerprint = f"{id_type.lower()}:{clean_id}".encode("utf-8")
        id_hash = hashlib.sha256(raw_fingerprint).hexdigest()

        from app.database import lookup_id_hashes, register_id_hash
        existing = lookup_id_hashes(id_hash)

        flags = []
        is_duplicate = False
        details = "No duplicates found. First-time registration."

        if existing:
            is_duplicate = True
            names_on_file = [row["registrant_name"].strip().lower() for row in existing]
            same_person = any(clean_name in n or n in clean_name for n in names_on_file)

            if not same_person:
                # Impersonation / Shared ID fraud
                flags.append("duplicate_id_different_name")
                prior_names = ", ".join([row["registrant_name"] for row in existing])
                details = f"FRAUD ALERT: This {id_type.upper()} was previously used by: {prior_names}"
            else:
                # Same user trying to register again
                flags.append("user_already_registered")
                prev_date = existing[0].get("created_at", "recently")
                details = f"User Already Entered: A registration with this ID was already submitted on {prev_date}."
        else:
            # Register this new ID hash
            masked_id = f"****{clean_id[-4:]}" if len(clean_id) >= 4 else clean_id
            register_id_hash(id_hash, id_type, masked_id, registrant_name, registration_id, event_id)

        return {
            "is_duplicate": is_duplicate,
            "hash": id_hash,
            "flags": flags,
            "details": details
        }

def check_duplicate(
    id_type: Optional[str],
    id_number: Optional[str],
    registrant_name: str,
    registration_id: str,
    event_id: Optional[str] = None
) -> Dict[str, Any]:
    detector = DuplicateDetector()
    return detector.check_and_register(id_type, id_number, registrant_name, registration_id, event_id)
