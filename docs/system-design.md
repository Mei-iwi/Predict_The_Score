# Thiết kế hệ thống

## Kiến trúc tổng thể

Hệ thống tách thành frontend, ML backend và database:

- Frontend ASP.NET Core MVC hiển thị form, nhận input và hiển thị kết quả.
- FastAPI backend phục vụ model machine learning.
- MySQL lưu lịch sử dự đoán để frontend có thể tải lại.

Sơ đồ Mermaid có tại:

- `reports/figures/architecture_diagram.mmd`
- `reports/figures/prediction_flow.mmd`

## Backend FastAPI

Các endpoint chính:

| Endpoint | Method | Vai trò |
| --- | --- | --- |
| `/health` | GET | Kiểm tra API còn hoạt động và model có load được không |
| `/model-info` | GET | Trả thông tin model, feature names, target, metrics |
| `/predict` | POST | Nhận input, validate, dự đoán điểm |

Validation input:

- `studytime`: 1-4
- `failures`: 0-4
- `absences`: 0-93
- `schoolsup`, `famsup`, `internet`: 0 hoặc 1

## Frontend MVC

Luồng trong frontend:

1. `Index.cshtml` hiển thị form.
2. `script.js` validate input và gửi JSON đến `/Predict/Submit`.
3. `PredictController` gọi `MlApiClient`.
4. `MlApiClient` gọi FastAPI `/predict`.
5. `PredictionHistoryService` lưu kết quả vào MySQL.
6. `/Predict/History` trả lịch sử mới nhất cho giao diện.

## Phần mở rộng scenario

Frontend có nút **Nâng cấp mô hình dự đoán**. Khi mở, người dùng chọn `web_minimal`, `early_warning` hoặc `reference`. JavaScript ẩn/hiện field theo scenario rồi gửi JSON đến MVC. MVC chuyển payload sang FastAPI. FastAPI nạp artifact theo scenario:

- `model_web_minimal.joblib`
- `model_early_warning.joblib`
- `model_reference.joblib`

Nếu artifact nâng cao chưa tồn tại, API trả lỗi rõ và hướng dẫn train model tương ứng.

## Database

Bảng chính là `PredictionHistory`. Bảng lưu tên học sinh, lớp, input, điểm dự đoán thang 20, điểm quy đổi thang 10, tên model và thời gian tạo.

SQL khởi tạo nằm ở `database/schema/001_init.sql`.

Cột `Scenario` lưu kịch bản dự đoán. Với database cũ, chạy `database/migrations/003_add_scenario.sql`.
