import pytest
import numpy as np
import cv2
import tempfile
import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def sample_id_image():
    # Create valid synthetic test image with text
    img = np.ones((500, 500, 3), dtype=np.uint8) * 255
    cv2.putText(img, "GOVERNMENT OF INDIA", (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(img, "ARJUN KUMAR", (40, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(img, "DOB: 14/05/1998", (40, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(img, "3675 9834 6012", (40, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    # Face silhouette placeholder
    cv2.circle(img, (380, 150), 50, (100, 100, 100), -1)

    path = os.path.join(tempfile.gettempdir(), "test_e2e_id.jpg")
    cv2.imwrite(path, img)

    yield path

    if os.path.exists(path):
        os.remove(path)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_verify_pipeline_e2e(sample_id_image):
    with open(sample_id_image, "rb") as f:
        response = client.post(
            "/api/v1/verify",
            files={"id_image": ("id.jpg", f, "image/jpeg")},
            data={
                "form_name": "Arjun Kumar",
                "form_email": "arjun@example.com",
                "form_dob": "1998-05-14",
                "event_id": "hackathon-2026"
            }
        )

    assert response.status_code == 200
    data = response.json()
    assert "registration_id" in data
    assert data["decision"] in ["approved", "manual_review", "rejected"]
    assert 0.0 <= data["confidence"] <= 1.0
    assert len(data["reason"]) > 0

def test_registrations_listing():
    response = client.get("/api/v1/registrations")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert isinstance(data["registrations"], list)
