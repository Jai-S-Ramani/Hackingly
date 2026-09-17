from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import os
import re
from app.config import config

class BaseOCRAdapter(ABC):
    @abstractmethod
    def extract_text(self, image_path: str) -> List[Dict[str, Any]]:
        """
        Extracts raw text blocks from image.
        Returns list of:
        {
            "text": str,
            "confidence": float,
            "bbox": Optional[List]
        }
        """
        pass

class EasyOCRAdapter(BaseOCRAdapter):
    def __init__(self, languages: Optional[List[str]] = None):
        self.languages = languages or config["ocr"].get("languages", ["en", "hi"])
        self.reader = None

    def _get_reader(self):
        if self.reader is None:
            try:
                import easyocr
                self.reader = easyocr.Reader(self.languages, gpu=False)
            except Exception as e:
                # Log or print warning; will fallback
                raise RuntimeError(f"Failed to initialize EasyOCR: {e}")
        return self.reader

    def extract_text(self, image_path: str) -> List[Dict[str, Any]]:
        try:
            reader = self._get_reader()
            results = reader.readtext(image_path)
            extracted = []
            for bbox, text, confidence in results:
                extracted.append({
                    "text": text.strip(),
                    "confidence": float(confidence),
                    "bbox": [list(pt) for pt in bbox] if bbox is not None else None
                })
            return extracted
        except Exception as e:
            # Return empty or fallback
            return [{"text": f"Error running EasyOCR: {str(e)}", "confidence": 0.0, "bbox": None}]

class MockOCRAdapter(BaseOCRAdapter):
    """Fallback / testing OCR adapter for unit testing without downloading multi-GB weights."""
    def __init__(self):
        pass

    def extract_text(self, image_path: str) -> List[Dict[str, Any]]:
        # Check filename or mock standard Indian ID text
        fname = os.path.basename(image_path).lower()
        if "pan" in fname:
            return [
                {"text": "INCOME TAX DEPARTMENT", "confidence": 0.95, "bbox": None},
                {"text": "GOVT. OF INDIA", "confidence": 0.95, "bbox": None},
                {"text": "Permanent Account Number Card", "confidence": 0.90, "bbox": None},
                {"text": "ABCDE1234F", "confidence": 0.96, "bbox": None},
                {"text": "ARJUN KUMAR", "confidence": 0.93, "bbox": None},
                {"text": "14/05/1998", "confidence": 0.94, "bbox": None},
            ]
        elif "voter" in fname:
            return [
                {"text": "ELECTION COMMISSION OF INDIA", "confidence": 0.95, "bbox": None},
                {"text": "ELECTOR PHOTO IDENTITY CARD", "confidence": 0.92, "bbox": None},
                {"text": "WKP4928174", "confidence": 0.96, "bbox": None},
                {"text": "KAVITA PATEL", "confidence": 0.93, "bbox": None},
                {"text": "30/07/1999", "confidence": 0.91, "bbox": None},
            ]
        elif "underage" in fname:
            return [
                {"text": "Government of India", "confidence": 0.95, "bbox": None},
                {"text": "ROHAN DAS", "confidence": 0.92, "bbox": None},
                {"text": "DOB: 12/09/2010", "confidence": 0.94, "bbox": None},
                {"text": "MALE", "confidence": 0.90, "bbox": None},
                {"text": "7829 4018 2741", "confidence": 0.93, "bbox": None},
            ]
        elif "college" in fname or "student" in fname:
            return [
                {"text": "INDIAN INSTITUTE OF TECHNOLOGY", "confidence": 0.95, "bbox": None},
                {"text": "STUDENT IDENTITY CARD", "confidence": 0.90, "bbox": None},
                {"text": "Name: RAHUL VERMA", "confidence": 0.92, "bbox": None},
                {"text": "Roll No: 2021CS10452", "confidence": 0.91, "bbox": None},
                {"text": "Valid Upto: 2026", "confidence": 0.88, "bbox": None},
            ]
        else: # Default Aadhaar
            return [
                {"text": "Government of India", "confidence": 0.95, "bbox": None},
                {"text": "ARJUN KUMAR", "confidence": 0.92, "bbox": None},
                {"text": "DOB: 14/05/1998", "confidence": 0.95, "bbox": None},
                {"text": "MALE", "confidence": 0.90, "bbox": None},
                {"text": "2345 6789 0124", "confidence": 0.94, "bbox": None},
            ]

class TextractOCRAdapter(BaseOCRAdapter):
    """Adapter for AWS Textract pipeline provided by Hackingly at the venue."""
    def __init__(self, region: str = "ap-south-1"):
        self.region = region

    def extract_text(self, image_path: str) -> List[Dict[str, Any]]:
        try:
            import boto3
            client = boto3.client("textract", region_name=self.region)
            with open(image_path, "rb") as document:
                response = client.detect_document_text(Document={"Bytes": document.read()})
            extracted = []
            for item in response.get("Blocks", []):
                if item["BlockType"] == "LINE":
                    extracted.append({
                        "text": item.get("Text", ""),
                        "confidence": float(item.get("Confidence", 0.0)) / 100.0,
                        "bbox": None
                    })
            return extracted
        except Exception as e:
            return [{"text": f"AWS Textract Error: {str(e)}", "confidence": 0.0, "bbox": None}]

def get_ocr_adapter(engine_name: Optional[str] = None) -> BaseOCRAdapter:
    engine = engine_name or config["ocr"].get("engine", "easyocr")
    if engine.lower() == "mock":
        return MockOCRAdapter()
    elif engine.lower() == "textract":
        return TextractOCRAdapter()
    else:
        # Default easyocr, fallback to mock if easyocr fails to import
        try:
            import easyocr
            return EasyOCRAdapter()
        except ImportError:
            return MockOCRAdapter()
