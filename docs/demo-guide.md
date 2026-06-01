# Demo guide

## Chuẩn bị trước demo

1. Chạy lại data pipeline và train model.
2. Chạy FastAPI backend.
3. Chạy MySQL.
4. Chạy ASP.NET Core MVC frontend.
5. Mở Swagger và giao diện web.

## Lệnh kiểm tra nhanh

```bash
python scripts/build_dataset.py
python scripts/train_model.py --scenario web_minimal
python scripts/evaluate_model.py
python scripts/compare_models.py
pytest ml-service/tests
dotnet build webapp/PredictTheScore.Web/PredictTheScore.Web.csproj
```

## Demo backend

```bash
cd ml-service
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Mở:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/model-info`

## Demo frontend

```bash
cd webapp/PredictTheScore.Web
dotnet run
```

Các bước thao tác:

1. Nhập tên học sinh và lớp.
2. Chọn `studytime`, `schoolsup`, `famsup`, `internet`.
3. Nhập `absences` và `failures`.
4. Bấm gửi dự đoán.
5. Kiểm tra điểm thang 20, điểm thang 10 và bảng lịch sử.

## Ảnh cần chụp

- Giao diện form trước khi nhập.
- Kết quả sau khi dự đoán thành công.
- Bảng lịch sử có dòng mới.
- Swagger `/docs` hiển thị schema request/response.
- `/model-info` trả feature names và metrics.
- Docker hoặc terminal cho thấy backend/frontend/database đang chạy.

