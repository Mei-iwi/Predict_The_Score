import sys
from pathlib import Path

from fastapi.testclient import TestClient

SERVICE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVICE_DIR))

from app.main import app

client = TestClient(app)


VALID_PAYLOAD = {
    "studytime": 2,
    "failures": 0,
    "absences": 4,
    "schoolsup": 1,
    "famsup": 1,
    "internet": 1,
}


def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200


def test_model_info_returns_model_information():
    response = client.get("/model-info")
    assert response.status_code == 200
    data = response.json()
    assert data["model_name"]
    assert data["feature_names"]
    assert data["target"] == "G3"


def test_predict_valid_input_returns_200():
    response = client.post("/predict", json=VALID_PAYLOAD)

    assert response.status_code == 200
    data = response.json()
    assert data["model_name"]
    assert data["message"]
    assert 0 <= data["predicted_score"] <= 20
    assert 0 <= data["predicted_score_10"] <= 10


def test_predict_invalid_studytime_returns_422():
    payload = {**VALID_PAYLOAD, "studytime": 9}
    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_missing_required_field_returns_422():
    payload = VALID_PAYLOAD.copy()
    payload.pop("internet")
    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predicted_score_is_between_0_and_20():
    response = client.post("/predict", json=VALID_PAYLOAD)
    assert response.status_code == 200

    assert 0 <= response.json()["predicted_score"] <= 20


def test_predicted_score_10_is_between_0_and_10():
    response = client.post("/predict", json=VALID_PAYLOAD)
    assert response.status_code == 200

    assert 0 <= response.json()["predicted_score_10"] <= 10
