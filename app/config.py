import os
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.yaml"

DEFAULT_CONFIG = {
    "ocr": {
        "engine": "easyocr",
        "languages": ["en", "hi"],
        "confidence_threshold": 0.50,
    },
    "quality": {
        "blur_threshold": 100.0,
        "min_width": 300,
        "min_height": 400,
        "ela_threshold": 15.0,
    },
    "face_match": {
        "model_name": "ArcFace",
        "detector_backend": "opencv",
        "threshold_match": 0.60,
        "threshold_uncertain": 0.40,
    },
    "name_match": {
        "threshold_match": 85.0,
        "threshold_uncertain": 65.0,
    },
    "decision": {
        "weights": {
            "quality": 0.10,
            "ocr": 0.20,
            "face": 0.30,
            "name": 0.25,
            "duplicate": 0.15,
        },
        "approve_threshold": 0.75,
        "review_threshold": 0.50,
    },
    "database": {
        "provider": os.getenv("DATABASE_PROVIDER", "supabase"),
        "db_path": str(BASE_DIR / "data" / "verifyai.db"),
        "supabase_url": os.getenv("SUPABASE_URL", "https://ejchzurnyvzhqcsqmbrl.supabase.co"),
        "supabase_key": os.getenv("SUPABASE_KEY", "sb_publishable_Gpbr08o4g-iXHyqHTxumlg_uX0HfV5L"),
    },
    "server": {
        "host": "0.0.0.0",
        "port": 8000,
    },
}

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

def load_config() -> dict:
    # Check env vars first
    base = DEFAULT_CONFIG.copy()
    if os.getenv("SUPABASE_URL"):
        base["database"]["supabase_url"] = os.getenv("SUPABASE_URL")
    if os.getenv("SUPABASE_KEY"):
        base["database"]["supabase_key"] = os.getenv("SUPABASE_KEY")
    if os.getenv("DATABASE_PROVIDER"):
        base["database"]["provider"] = os.getenv("DATABASE_PROVIDER")

    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
            # Deep merge defaults
            merged = base.copy()
            for k, v in user_config.items():
                if isinstance(v, dict) and k in merged:
                    merged[k].update(v)
                else:
                    merged[k] = v
            # Ensure env vars take precedence
            if os.getenv("SUPABASE_URL"):
                merged["database"]["supabase_url"] = os.getenv("SUPABASE_URL")
            if os.getenv("SUPABASE_KEY"):
                merged["database"]["supabase_key"] = os.getenv("SUPABASE_KEY")
            if os.getenv("DATABASE_PROVIDER"):
                merged["database"]["provider"] = os.getenv("DATABASE_PROVIDER")
            return merged
    return base

config = load_config()
