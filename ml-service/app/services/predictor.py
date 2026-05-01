from __future__ import annotations

from app.schemas.request import PredictionRequest
from app.services.model_loader import load_model_bundle
from app.services.preprocessing import build_input_dataframe


def predict_score(payload: PredictionRequest) -> float:
    bundle = load_model_bundle()

    model = bundle["model"]
    feature_names = bundle.get("feature_names", [
        "studytime",
        "failures",
        "absences",
        "schoolsup",
        "famsup",
        "internet",
    ])

    x = build_input_dataframe(payload, feature_names)
    score = float(model.predict(x)[0])

    return max(0.0, min(20.0, score))