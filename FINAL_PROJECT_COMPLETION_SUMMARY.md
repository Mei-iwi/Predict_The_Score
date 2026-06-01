# FINAL_PROJECT_COMPLETION_SUMMARY.md

## 1. Kết quả cập nhật

Project đã được kiểm tra và cập nhật để hỗ trợ 3 kịch bản dự đoán:

- `web_minimal`: mặc định, dùng 6 field cơ bản trên form.
- `early_warning`: thêm `subject`, `higher`, `traveltime`.
- `reference`: thêm `subject`, `higher`, `traveltime`, `G1`, `G2`.

Không ghi secret, mật khẩu database hoặc connection string thật vào file tổng kết này.

## 2. Artifact model

| Scenario | Artifact | Trạng thái |
| --- | --- | --- |
| `web_minimal` | `ml-service/artifacts/model_web_minimal.joblib` | Có |
| `early_warning` | `ml-service/artifacts/model_early_warning.joblib` | Có |
| `reference` | `ml-service/artifacts/model_reference.joblib` | Có |

## 3. Frontend scenario UI

Đã cập nhật giao diện trong `Views/Home/Index.cshtml` và `wwwroot/js/script.js`:

- Khi mở trang lần đầu: dùng `web_minimal`, ẩn selector scenario, ẩn và disable các field nâng cao.
- Nút `Nâng cấp mô hình dự đoán` hiển thị selector scenario và đổi thành `Thu gọn mô hình dự đoán`.
- Chọn `web_minimal`: chỉ gửi 6 field cơ bản.
- Chọn `early_warning`: chỉ hiện và gửi `subject`, `higher`, `traveltime`.
- Chọn `reference`: hiện và gửi `subject`, `higher`, `traveltime`, `G1`, `G2`.
- Khi thu gọn: reset về `web_minimal`, ẩn selector, ẩn và disable field nâng cao.

Các hàm JS chính đã có:

- `initScenarioUi()`
- `toggleAdvancedMode()`
- `updateScenarioFields()`
- `getSelectedScenario()`
- `buildPredictionPayload()`

## 4. Backend, MVC và database

- FastAPI nhận `scenario`, mặc định là `web_minimal`.
- `early_warning` yêu cầu thêm `subject`, `higher`, `traveltime`.
- `reference` yêu cầu thêm `subject`, `higher`, `traveltime`, `G1`, `G2`.
- MVC DTO/controller/client đã truyền scenario và field nâng cao.
- History đã có cột `Scenario`.
- Có migration `database/migrations/003_add_scenario.sql` cho database đã tồn tại.

## 5. Kiểm tra đã chạy

| Lệnh | Kết quả | Ghi chú |
| --- | --- | --- |
| `node --check webapp/PredictTheScore.Web/wwwroot/js/script.js` | Pass | JS không lỗi cú pháp |
| Kiểm tra artifact 3 model | Pass | Đủ 3 file `.joblib` |
| `docker compose config` | Pass | Compose parse được; không copy output có secret vào tài liệu |
| `dotnet build webapp/PredictTheScore.Web/PredictTheScore.Web.csproj` | Blocked | File Debug đang bị process `PredictTheScore.Web` giữ |
| `dotnet build webapp/PredictTheScore.Web/PredictTheScore.Web.csproj -c Release -p:UseAppHost=false` | Pass | 0 warning, 0 error |
| `python -m pytest ml-service/tests` | Failed | Python hiện tại thiếu package `pytest` |

## 6. Việc cần làm trước demo

- Nếu đang chạy webapp từ `bin/Debug`, dừng process `PredictTheScore.Web` rồi chạy lại `dotnet build` Debug nếu cần.
- Tạo/cài lại Python virtual environment theo README, sau đó chạy `python -m pytest ml-service/tests`.
- Với database đã có sẵn, chạy migration `database/migrations/003_add_scenario.sql` để thêm cột `Scenario`.
- Demo đủ 3 scenario trên giao diện và kiểm tra history lưu đúng scenario.
