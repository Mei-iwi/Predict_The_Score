import sys
from pathlib import Path

from fastapi.testclient import TestClient

SERVICE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVICE_DIR))

from app.main import app
from app.services.model_loader import get_model_path

client = TestClient(app)


VALID_PAYLOAD = {
    "studytime": 2,
    "failures": 0,
    "absences": 4,
    "schoolsup": 1,
    "famsup": 1,
    "internet": 1,
}

EARLY_WARNING_PAYLOAD = {
    **VALID_PAYLOAD,
    "scenario": "early_warning",
    "subject": "mat",
    "higher": 1,
    "traveltime": 2,
}

REFERENCE_PAYLOAD = {
    **EARLY_WARNING_PAYLOAD,
    "scenario": "reference",
    "G1": 12,
    "G2": 13,
}


def scenario_model_exists(scenario: str) -> bool:
    return get_model_path(scenario).exists()


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
    assert "web_minimal" in data["available_scenarios"]


def test_predict_valid_input_returns_200():
    response = client.post("/predict", json=VALID_PAYLOAD)

    assert response.status_code == 200
    data = response.json()
    assert data["model_name"]
    assert data["message"]
    assert data["scenario"] == "web_minimal"
    assert 0 <= data["predicted_score"] <= 20
    assert 0 <= data["predicted_score_20"] <= 20
    assert 0 <= data["predicted_score_10"] <= 10


def test_predict_without_scenario_uses_web_minimal():
    response = client.post("/predict", json=VALID_PAYLOAD)
    assert response.status_code == 200
    assert response.json()["scenario"] == "web_minimal"


def test_predict_web_minimal_scenario_returns_200():
    payload = {**VALID_PAYLOAD, "scenario": "web_minimal"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200


def test_predict_early_warning_returns_200_if_model_exists():
    if not scenario_model_exists("early_warning"):
        response = client.post("/predict", json=EARLY_WARNING_PAYLOAD)
        assert response.status_code == 503
        return

    response = client.post("/predict", json=EARLY_WARNING_PAYLOAD)
    assert response.status_code == 200
    assert response.json()["scenario"] == "early_warning"


def test_predict_reference_returns_200_if_model_exists():
    if not scenario_model_exists("reference"):
        response = client.post("/predict", json=REFERENCE_PAYLOAD)
        assert response.status_code == 503
        return

    response = client.post("/predict", json=REFERENCE_PAYLOAD)
    assert response.status_code == 200
    assert response.json()["scenario"] == "reference"


def test_predict_invalid_studytime_returns_422():
    payload = {**VALID_PAYLOAD, "studytime": 9}
    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_missing_required_field_returns_422():
    payload = VALID_PAYLOAD.copy()
    payload.pop("internet")
    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_invalid_scenario_returns_422():
    payload = {**VALID_PAYLOAD, "scenario": "wrong"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_missing_scenario_field_returns_422():
    payload = {**EARLY_WARNING_PAYLOAD}
    payload.pop("subject")
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_invalid_subject_returns_422():
    payload = {**EARLY_WARNING_PAYLOAD, "subject": "science"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_invalid_g1_g2_returns_422():
    payload = {**REFERENCE_PAYLOAD, "G1": 30}
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
