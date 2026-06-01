# API specification

## Base URL

Khi chạy local:

```text
http://127.0.0.1:8000
```

## GET /health

Kiểm tra backend còn hoạt động.

Response mẫu:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

## GET /model-info

Trả thông tin model đang phục vụ.

Response mẫu:

```json
{
  "model_name": "LinearRegression",
  "scenario": "web_minimal",
  "feature_names": ["studytime", "failures", "absences", "schoolsup", "famsup", "internet"],
  "target": "G3",
  "metrics": {
    "test": {
      "mae": 2.3173,
      "mse": 10.6394,
      "rmse": 3.2618,
      "r2": 0.0902
    }
  }
}
```

## POST /predict

Nhận thông tin học sinh và trả điểm dự đoán.

Request:

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

Validation:

| Field | Range |
| --- | --- |
| `studytime` | 1-4 |
| `failures` | 0-4 |
| `absences` | 0-93 |
| `schoolsup` | 0 hoặc 1 |
| `famsup` | 0 hoặc 1 |
| `internet` | 0 hoặc 1 |

Response:

```json
{
  "predicted_score": 12.8,
  "predicted_score_10": 6.4,
  "model_name": "LinearRegression",
  "message": "Prediction completed successfully."
}
```

Nếu input sai range hoặc thiếu field, FastAPI trả lỗi `422 Unprocessable Entity`.

