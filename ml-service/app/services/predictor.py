from __future__ import annotations

import pandas as pd

from app.schemas.request import PredictionRequest
from app.services.model_loader import load_model_bundle


def predict_score(payload: PredictionRequest) -> float:
    bundle = load_model_bundle()

    model = bundle["model"]
    feature_names = bundle.get("feature_names", [
        "studytime",
        "failures",
        "absences",
        "schoolsup",
        "famsup",
        "internet"
    ])

    input_values = {
        "studytime": payload.studytime,
        "failures": payload.failures,
        "absences": payload.absences,
        "schoolsup": payload.schoolsup,
        "famsup": payload.famsup,
        "internet": payload.internet,
    }

    x = pd.DataFrame([input_values])

    # Bắt buộc sắp xếp cột đúng thứ tự model đã train
    x = x[feature_names]

    if x.isna().any().any():
        raise ValueError(
            f"Dữ liệu đầu vào có giá trị NaN: {x.to_dict(orient='records')[0]}"
        )

    score = float(model.predict(x)[0])

    # Giới hạn điểm trong thang 0-20
    return max(0.0, min(20.0, score))