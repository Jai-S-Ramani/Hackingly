import io
import os
import base64
from pathlib import Path
from typing import Dict, Any, List, Tuple
import numpy as np
from PIL import Image, ImageChops, ImageEnhance, ExifTags
import cv2
from app.config import config

class QualityAnalyzer:
    def __init__(self):
        self.blur_threshold = config["quality"].get("blur_threshold", 100.0)
        self.min_width = config["quality"].get("min_width", 300)
        self.min_height = config["quality"].get("min_height", 400)
        self.ela_threshold = config["quality"].get("ela_threshold", 15.0)

    def analyze(self, image_path: str) -> Dict[str, Any]:
        """
        Stage 1 Quality & Forensics Analyzer:
        1. Blur detection (Laplacian variance)
        2. Glare & overexposure check
        3. Resolution & aspect ratio validation
        4. Error Level Analysis (ELA) with base64 visual heatmap
        5. EXIF digital editing software inspection
        """
        flags: List[str] = []
        blur_score = 0.0
        glare_score = 0.0
        resolution_ok = True
        tampering_score = 0.0
        ela_heatmap_base64 = None
        exif_flags = []
        quality_confidence = 1.0

        if not os.path.exists(image_path):
            return {
                "quality_passed": False,
                "blur_score": 0.0,
                "glare_score": 0.0,
                "resolution_ok": False,
                "tampering_score": 1.0,
                "flags": ["file_not_found"],
                "quality_confidence": 0.0,
                "detected_doc_type": "unknown",
                "ela_heatmap_base64": None
            }

        # 1. OpenCV Analysis: Blur, Glare, Resolution
        try:
            cv_img = cv2.imread(image_path)
            if cv_img is None:
                pil_temp = Image.open(image_path).convert("RGB")
                cv_img = np.array(pil_temp)[:, :, ::-1]

            height, width = cv_img.shape[:2]
            if width < self.min_width or height < self.min_height:
                resolution_ok = False
                flags.append("low_resolution")
                quality_confidence -= 0.3

            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            
            # Laplacian variance
            blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
            if blur_score < self.blur_threshold:
                flags.append("blurry_image")
                quality_confidence -= 0.4

            # Glare / overexposure check (pixels near pure white > 250)
            white_pixels = np.sum(gray >= 250)
            total_pixels = gray.size
            glare_score = float(white_pixels / total_pixels)
            if glare_score > 0.25:
                flags.append("high_glare_or_overexposed")
                quality_confidence -= 0.2

        except Exception as e:
            flags.append(f"quality_cv_error: {str(e)}")
            quality_confidence -= 0.2

        # 2. Error Level Analysis (ELA) with Heatmap Generation
        try:
            pil_img = Image.open(image_path).convert("RGB")
            tampering_score, is_suspicious, ela_heatmap_base64 = self._calculate_ela(pil_img)
            if is_suspicious:
                flags.append("potential_tampering_ela")
                quality_confidence -= 0.45
        except Exception as e:
            flags.append(f"quality_ela_error: {str(e)}")

        # 3. EXIF Metadata Inspection
        try:
            exif_flags = self._check_exif(image_path)
            if exif_flags:
                flags.extend(exif_flags)
                quality_confidence -= 0.35
        except Exception:
            pass

        quality_confidence = max(0.0, min(1.0, quality_confidence))
        quality_passed = ("blurry_image" not in flags and 
                          "low_resolution" not in flags and 
                          "potential_tampering_ela" not in flags)

        return {
            "quality_passed": quality_passed,
            "blur_score": round(blur_score, 2),
            "glare_score": round(glare_score, 3),
            "resolution_ok": resolution_ok,
            "tampering_score": round(tampering_score, 3),
            "flags": flags,
            "exif_flags": exif_flags,
            "quality_confidence": round(quality_confidence, 2),
            "ela_heatmap_base64": ela_heatmap_base64,
            "detected_doc_type": "indian_id",
        }

    def _calculate_ela(self, image: Image.Image, quality: int = 90) -> Tuple[float, bool, str]:
        """
        Error Level Analysis:
        Resaves image at 90% JPEG quality, computes absolute difference.
        Returns normalized score, suspicious boolean, and base64 heatmap image.
        """
        buffer = io.BytesIO()
        image.save(buffer, "JPEG", quality=quality)
        buffer.seek(0)
        resaved = Image.open(buffer)

        diff = ImageChops.difference(image, resaved)
        extrema = diff.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        scale = 255.0 / max(max_diff, 1)
        enhanced_diff = ImageEnhance.Brightness(diff).enhance(scale)

        diff_arr = np.array(enhanced_diff)
        mean_diff = float(np.mean(diff_arr))

        # Encode enhanced diff as base64 JPEG for organizer UI heatmap view
        out_buf = io.BytesIO()
        enhanced_diff.save(out_buf, format="JPEG")
        b64_str = base64.b64encode(out_buf.getvalue()).decode("utf-8")

        # Thresholds
        tampering_score = min(1.0, mean_diff / 45.0)
        is_suspicious = mean_diff > self.ela_threshold
        return tampering_score, is_suspicious, b64_str

    def _check_exif(self, image_path: str) -> List[str]:
        signatures = ["photoshop", "gimp", "canva", "snapseed", "picsart", "adobe", "lightroom", "pixlr"]
        detected = []
        try:
            with Image.open(image_path) as img:
                info = img._getexif()
                if info:
                    for tag_id, value in info.items():
                        tag_name = ExifTags.TAGS.get(tag_id, str(tag_id)).lower()
                        val_str = str(value).lower()
                        if any(k in tag_name for k in ["software", "processing", "artist", "model", "editor"]):
                            for sig in signatures:
                                if sig in val_str:
                                    detected.append(f"editing_software_{sig}")
        except Exception:
            pass
        return detected

def check_quality_and_tampering(image_path: str) -> Dict[str, Any]:
    analyzer = QualityAnalyzer()
    return analyzer.analyze(image_path)
