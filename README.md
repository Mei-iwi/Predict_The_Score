# Predict The Score

Ứng dụng dự đoán điểm cuối kỳ `G3` của học sinh bằng mô hình hồi quy tuyến tính. Project dùng dữ liệu UCI Student Performance, backend FastAPI, frontend ASP.NET Core MVC và MySQL để lưu lịch sử dự đoán.

## 1. Mục tiêu

- Làm sạch và phân tích dữ liệu học sinh.
- Huấn luyện mô hình hồi quy để dự đoán điểm `G3` trên thang 20.
- Hiển thị thêm điểm quy đổi thang 10 trên giao diện web.
- Lưu lịch sử dự đoán gồm thông tin học sinh, input, điểm dự đoán, model và thời gian tạo.

## 2. Kiến trúc

```text
Browser
  -> ASP.NET Core MVC webapp
  -> FastAPI ml-service
  -> LinearRegression model.joblib

ASP.NET Core MVC webapp
  -> MySQL PredictionHistory
```

## 3. Công nghệ

- Python, pandas, scikit-learn, matplotlib, FastAPI, Pydantic, joblib
- ASP.NET Core MVC, Razor, JavaScript, CSS
- MySQL, MySqlConnector
- Docker Compose

## 4. Cấu trúc chính

```text
data/raw/                         Dữ liệu gốc UCI
data/processed/                   Dữ liệu sạch và feature_config.json
scripts/                          Data processing, training, evaluation
ml-service/                       FastAPI prediction backend
webapp/PredictTheScore.Web/       ASP.NET Core MVC frontend
database/schema/                  SQL tạo bảng PredictionHistory
reports/figures/                  Hình dùng cho báo cáo
reports/tables/                   Bảng metrics, correlation, comparison
docs/                             Tài liệu kiến trúc, API, dữ liệu, demo
tests/manual/                     Checklist kiểm thử thủ công
```

## 5. Chuẩn bị Python

Tạo môi trường ảo và cài thư viện:

```bash
cd ml-service
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cd ..
```

Nếu dùng Git Bash, lệnh kích hoạt có thể là:

```bash
source ml-service/.venv/Scripts/activate
```

## 6. Xử lý dữ liệu và huấn luyện

Chạy từ thư mục gốc project:

```bash
python scripts/build_dataset.py
python scripts/train_model.py --scenario web_minimal
python scripts/evaluate_model.py
python scripts/compare_models.py
```

Các output quan trọng:

- `data/processed/student_performance_clean.csv`
- `reports/processing_audit.json`
- `reports/tables/pearson_correlation.csv`
- `reports/tables/model_comparison.csv`
- `reports/tables/model_coefficients.csv`
- `ml-service/artifacts/model.joblib`

## 7. Chạy backend FastAPI

```bash
cd ml-service
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

URL kiểm tra:

- API root: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`
- Model info: `http://127.0.0.1:8000/model-info`

## 8. Chạy frontend ASP.NET Core MVC

```bash
cd webapp/PredictTheScore.Web
dotnet run
```

Mở URL mà `dotnet run` in ra, thường là `http://localhost:5000` hoặc `https://localhost:5001`.

Frontend gửi form đến `/Predict/Submit`, MVC controller gọi FastAPI `/predict`, sau đó lưu kết quả vào MySQL.

## 9. Chạy bằng Docker Compose

```bash
docker compose up --build
```

Docker Compose có các service:

- `db`: MySQL
- `ml-service`: FastAPI backend
- `webapp`: ASP.NET Core MVC frontend

Không đưa mật khẩu thật trong file cấu hình vào báo cáo hoặc slide. Khi trình bày, chỉ mô tả là project dùng connection string local/Docker.

## 10. Kiểm thử

```bash
pytest ml-service/tests
dotnet build webapp/PredictTheScore.Web/PredictTheScore.Web.csproj
```

Checklist thủ công nằm ở `tests/manual/test_cases.md`.

## 11. API chính

Request `POST /predict`:

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

Response:

```json
{
  "predicted_score": 12.8,
  "predicted_score_10": 6.4,
  "model_name": "LinearRegression",
  "message": "Prediction completed successfully."
}
```

## 12. Ghi chú báo cáo

- Model chính của app là `LinearRegression` với scenario `web_minimal` vì khớp 6 trường đang có trên form web.
- Scenario `reference` có độ chính xác cao hơn vì dùng thêm `G1`, `G2`, nhưng hiện form web chưa thu thập các điểm này.
- Các mục cần nhóm tự bổ sung trước khi nộp: tên thành viên thật, ảnh screenshot demo, slide PowerPoint và link commit minh chứng.
