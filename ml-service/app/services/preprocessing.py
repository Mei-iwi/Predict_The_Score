from __future__ import annotations

import pandas as pd

from app.schemas.request import PredictionRequest


def build_input_dataframe(payload: PredictionRequest, feature_names: list[str]) -> pd.DataFrame:
    input_values = {
        "studytime": payload.studytime,
        "failures": payload.failures,
        "absences": payload.absences,
        "schoolsup": payload.schoolsup,
        "famsup": payload.famsup,
        "internet": payload.internet,
    }

    missing_features = [name for name in feature_names if name not in input_values]
    if missing_features:
        raise ValueError(f"Request thiếu feature cần cho model: {missing_features}")

    x = pd.DataFrame([input_values])
    x = x[feature_names]

    if x.isna().any().any():
        raise ValueError(f"Dữ liệu đầu vào có NaN: {x.to_dict(orient='records')[0]}")

    return x