from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_predict_valid_input():
    payload = {
        "studytime": 2,
        "failures": 0,
        "absences": 4,
        "schoolsup": 1,
        "famsup": 1,
        "internet": 1,
    }
    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "predicted_score" in data
    assert "model_name" in data
    assert 0 <= data["predicted_score"] <= 20


def test_predict_invalid_studytime():
    payload = {
        "studytime": 9,
        "failures": 0,
        "absences": 4,
        "schoolsup": 1,
        "famsup": 1,
        "internet": 1,
    }
    response = client.post("/predict", json=payload)

    assert response.status_code == 422