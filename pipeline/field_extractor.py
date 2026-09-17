import re
from datetime import datetime
from typing import List, Dict, Any, Optional

# --- Verhoeff Checksum Algorithm for Aadhaar ---
VERHOEFF_D = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 6, 7, 8, 9, 0, 1, 2, 3, 4],
    [6, 7, 8, 9, 5, 1, 2, 3, 4, 0],
    [7, 8, 9, 5, 6, 2, 3, 4, 0, 1],
    [8, 9, 5, 6, 7, 3, 4, 0, 1, 2],
    [9, 5, 6, 7, 8, 4, 0, 1, 2, 3]
]

VERHOEFF_P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
]

VERHOEFF_INV = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]

def validate_verhoeff_aadhaar(aadhaar_num: str) -> bool:
    """Validates 12-digit Aadhaar number using standard Verhoeff checksum algorithm."""
    clean = re.sub(r"\D", "", aadhaar_num)
    if len(clean) != 12:
        return False
    c = 0
    reversed_digits = [int(x) for x in reversed(clean)]
    for i, digit in enumerate(reversed_digits):
        c = VERHOEFF_D[c][VERHOEFF_P[i % 8][digit]]
    return c == 0

def mask_id_number(id_num: str) -> str:
    """Masks ID number to only show last 4 characters for security."""
    clean = re.sub(r"\s+", "", id_num)
    if len(clean) <= 4:
        return clean
    return f"****{clean[-4:]}"

class FieldExtractor:
    def __init__(self):
        # Indian Aadhaar numbers always begin with digits 2-9
        self.aadhaar_regex = re.compile(r"\b[2-9]\d{3}\s?\d{4}\s?\d{4}\b")
        self.pan_regex = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b")
        self.voter_regex = re.compile(r"\b[A-Z]{3}[0-9]{7}\b")
        self.roll_regex = re.compile(r"\b(?:roll\s*(?:no\.?|number)?[:\s]*)?([A-Z0-9]{6,15})\b", re.IGNORECASE)
        self.dob_regex = re.compile(r"(?:dob|d\.o\.b|date of birth|year of birth|birth|जन्म तिथि|जन्मतारीख)[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4})", re.IGNORECASE)
        self.general_date_regex = re.compile(r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b")

    def parse_blocks(self, blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        full_text = " ".join([b["text"] for b in blocks])
        lines = [b["text"].strip() for b in blocks if b["text"].strip()]

        id_type = self._classify_document(full_text)
        dob, birth_year = self._extract_dob(full_text)
        id_number = self._extract_id_number(full_text, id_type)
        name = self._extract_name(lines, id_type)
        institution = self._extract_institution(lines) if id_type == "college_id" else None
        valid_upto = self._extract_validity(full_text) if id_type == "college_id" else None

        format_valid = True
        checksum_valid = None

        if id_type == "aadhaar" and id_number:
            checksum_valid = validate_verhoeff_aadhaar(id_number)
            format_valid = bool(re.match(r"^[2-9]\d{3}\s?\d{4}\s?\d{4}$", id_number))
        elif id_type == "pan" and id_number:
            format_valid = bool(self.pan_regex.match(id_number))
            checksum_valid = True
        elif id_type == "voter_id" and id_number:
            format_valid = bool(self.voter_regex.match(id_number))
            checksum_valid = True

        extraction_confidence = 0.85
        if not id_number:
            extraction_confidence -= 0.3
        if not dob and not birth_year and id_type != "college_id":
            extraction_confidence -= 0.2
        if not name:
            extraction_confidence -= 0.2
        if checksum_valid is False:
            extraction_confidence -= 0.3

        return {
            "name": name,
            "date_of_birth": dob,
            "birth_year": birth_year,
            "id_number": id_number,
            "id_number_masked": mask_id_number(id_number) if id_number else None,
            "id_type": id_type,
            "institution": institution,
            "valid_upto": valid_upto,
            "format_valid": format_valid,
            "checksum_valid": checksum_valid,
            "extraction_confidence": max(0.1, round(extraction_confidence, 2)),
            "raw_text": full_text[:600],
        }

    def _classify_document(self, text: str) -> str:
        t_low = text.lower()
        if "income tax department" in t_low or "permanent account number" in t_low or self.pan_regex.search(text):
            return "pan"
        elif any(k in t_low for k in ["government of india", "unique identification", "aadhaar", "uidai", "मेरा आधार"]):
            return "aadhaar"
        elif any(k in t_low for k in ["student", "college", "university", "institute", "roll no", "identity card", "campus", "faculty"]):
            return "college_id"
        elif any(k in t_low for k in ["election commission", "voter", "epic", "elector"]):
            return "voter_id"
        return "indian_id"

    def _extract_dob(self, text: str) -> Tuple[Optional[str], Optional[int]]:
        # Check prefix match first (DOB: ...)
        match = self.dob_regex.search(text)
        if match:
            val = match.group(1).replace("-", "/")
            if "/" in val:
                parts = val.split("/")
                if len(parts) == 3:
                    d, m, y = parts[0], parts[1], parts[2]
                    if len(y) == 2:
                        y = f"19{y}" if int(y) > 30 else f"20{y}"
                    try:
                        dt = datetime(int(y), int(m), int(d))
                        return dt.strftime("%Y-%m-%d"), int(y)
                    except Exception:
                        pass
            elif len(val) == 4 and val.isdigit():
                return None, int(val)

        # General date fallback
        for gm in self.general_date_regex.finditer(text):
            raw = gm.group(1).replace("-", "/")
            parts = raw.split("/")
            if len(parts) == 3:
                d, m, y = parts[0], parts[1], parts[2]
                if len(y) == 4 and 1940 <= int(y) <= 2015:
                    try:
                        dt = datetime(int(y), int(m), int(d))
                        return dt.strftime("%Y-%m-%d"), int(y)
                    except Exception:
                        pass
        return None, None

    def _extract_id_number(self, text: str, doc_type: str) -> Optional[str]:
        if doc_type == "pan":
            m = self.pan_regex.search(text)
            if m:
                return m.group(0)
        elif doc_type == "aadhaar":
            m = self.aadhaar_regex.search(text)
            if m:
                return m.group(0)
        elif doc_type == "voter_id":
            m = self.voter_regex.search(text)
            if m:
                return m.group(0)
        elif doc_type == "college_id":
            for m in self.roll_regex.finditer(text):
                val = m.group(1)
                if any(c.isdigit() for c in val) and len(val) >= 6:
                    return val

        # Fallbacks
        pan_m = self.pan_regex.search(text)
        if pan_m:
            return pan_m.group(0)
        aadhaar_m = self.aadhaar_regex.search(text)
        if aadhaar_m:
            return aadhaar_m.group(0)
        voter_m = self.voter_regex.search(text)
        if voter_m:
            return voter_m.group(0)
        return None

    def _extract_name(self, lines: List[str], doc_type: str) -> Optional[str]:
        noise = [
            "government", "india", "income", "tax", "department", "dob", "date",
            "birth", "male", "female", "card", "permanent", "account", "identity",
            "student", "roll", "valid", "upto", "father", "mother", "husband",
            "s/o", "d/o", "w/o", "signature", "uidai", "help", "www", "enrolment"
        ]
        candidates = []
        for i, line in enumerate(lines):
            l_clean = re.sub(r"[^A-Za-z\s]", "", line).strip()
            l_low = l_clean.lower()
            
            # Skip noise or relative prefix lines
            if any(k in l_low for k in ["father's name", "father name", "s/o", "d/o", "w/o"]):
                continue

            if len(l_clean) > 3 and not any(k in l_low for k in noise):
                words = l_clean.split()
                if 1 <= len(words) <= 4:
                    candidates.append(l_clean)

        if candidates:
            return candidates[0].upper()
        return None

    def _extract_institution(self, lines: List[str]) -> Optional[str]:
        keywords = ["institute", "university", "college", "school", "technology", "engineering", "iit", "nit", "bits", "iiit", "vit"]
        for line in lines:
            if any(k in line.lower() for k in keywords):
                return line.strip()
        return None

    def _extract_validity(self, text: str) -> Optional[str]:
        m = re.search(r"(?:valid\s*(?:upto|thru|until|till)?[:\s]*)(\d{4})", text, re.IGNORECASE)
        if m:
            return m.group(1)
        return None

def extract_id_fields(blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
    extractor = FieldExtractor()
    return extractor.parse_blocks(blocks)
