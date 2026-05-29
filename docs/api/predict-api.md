# Predict API

Base URL for local FastAPI backend: `http://127.0.0.1:8000`

Swagger UI: `http://127.0.0.1:8000/docs`

## Health

`GET /health`

Example response:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

## Model info

`GET /model-info`

Example response:

```json
{
  "model_name": "LinearRegression-web_minimal",
  "scenario": "web_minimal",
  "feature_names": ["studytime", "failures", "absences", "schoolsup", "famsup", "internet"],
  "target": "G3",
  "metrics": {
    "train": {},
    "test": {}
  }
}
```

## Predict

`POST /predict`

Request body:

```json
{
  "studytime": 2,
  "failures": 0,
  "absences": 4,
  "schoolsup": 1,
  "famsup": 1,
  "internet": 1
}
```

Validation rules:

- `studytime`: 1 to 4
- `failures`: 0 to 4
- `absences`: 0 to 93
- `schoolsup`: 0 or 1
- `famsup`: 0 or 1
- `internet`: 0 or 1

Example response:

```json
{
  "predicted_score": 12.8,
  "predicted_score_10": 6.4,
  "model_name": "LinearRegression-web_minimal",
  "message": "Prediction completed successfully."
}
```
