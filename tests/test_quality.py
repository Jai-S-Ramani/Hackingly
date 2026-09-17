import pytest
import numpy as np
import cv2
import tempfile
import os
from PIL import Image
from pipeline.quality_analyzer import QualityAnalyzer

@pytest.fixture
def temp_images():
    # 1. Clear sharp image
    img = np.ones((500, 500, 3), dtype=np.uint8) * 200
    # Add high frequency patterns/text for sharpness
    cv2.putText(img, "VERIFYAI TEST AADHAAR CARD", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(img, "GOVERNMENT OF INDIA", (50, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.rectangle(img, (50, 200), (250, 400), (50, 50, 50), -1)

    sharp_path = os.path.join(tempfile.gettempdir(), "test_sharp.jpg")
    cv2.imwrite(sharp_path, img)

    # 2. Heavily blurred image
    blurry_img = cv2.GaussianBlur(img, (45, 45), 0)
    blur_path = os.path.join(tempfile.gettempdir(), "test_blurry.jpg")
    cv2.imwrite(blur_path, blurry_img)

    yield sharp_path, blur_path

    for p in [sharp_path, blur_path]:
        if os.path.exists(p):
            os.remove(p)

def test_sharp_image_passes(temp_images):
    sharp_path, _ = temp_images
    analyzer = QualityAnalyzer()
    res = analyzer.analyze(sharp_path)
    assert res["resolution_ok"] is True
    assert res["blur_score"] > 50.0

def test_blurry_image_fails_or_flags(temp_images):
    _, blur_path = temp_images
    analyzer = QualityAnalyzer()
    res = analyzer.analyze(blur_path)
    assert "blurry_image" in res["flags"]
    assert res["blur_score"] < 50.0
