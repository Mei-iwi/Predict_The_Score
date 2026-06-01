# REPORT_SOURCE_MATERIAL_UPDATED.md

Tài liệu này là nguồn nội dung để viết báo cáo Word. Nội dung chỉ dựa trên file hiện có trong project; phần thiếu được ghi rõ là **Need confirmation** hoặc **Not found in current project**.

## 1. Lịch làm việc nhóm theo tuần

| Tuần | Công việc | Kết quả | Minh chứng |
| --- | --- | --- | --- |
| Week 01 | Tìm hiểu dataset, xác định target `G3`, tạo cấu trúc project | Có dữ liệu thô và hướng xử lý ban đầu | `docs/progress/week-01.md` |
| Week 02 | Train baseline, tạo API, kết nối frontend | Có `LinearRegression`, FastAPI `/predict`, form web | `docs/progress/week-02.md` |
| Week 03 | Bổ sung audit, charts, model comparison, history, tests | Có reports, API rõ hơn, lưu lịch sử | `docs/progress/week-03.md` |

Người phụ trách cụ thể: **Need confirmation**.

## 2. Phân công công việc thành viên

Thông tin thành viên chính thức chưa có trong repository. Dùng `docs/teamwork.md` để điền tên, vai trò và commit evidence trước khi nộp.

## 3. Giới thiệu đề tài

Đề tài **Xây dựng ứng dụng để dự đoán điểm số của học sinh** thuộc môn Khai phá dữ liệu. Project dùng dữ liệu UCI Student Performance để dự đoán điểm cuối kỳ `G3` trên thang 20, sau đó quy đổi thêm sang thang 10 cho giao diện. Hệ thống gồm pipeline xử lý dữ liệu, mô hình hồi quy, FastAPI backend, ASP.NET Core MVC frontend và MySQL để lưu lịch sử dự đoán.

## 4. Cơ sở lý thuyết

Bài toán được mô hình hóa dưới dạng hồi quy vì output là điểm số liên tục. Model chính là `LinearRegression`, dễ giải thích bằng hệ số của từng biến. Project dùng Pearson correlation để phân tích liên hệ tuyến tính giữa các biến và dùng MAE, MSE, RMSE, R2 để đánh giá mô hình.

## 5. Phân tích dữ liệu

Dữ liệu gồm `student-mat.csv` và `student-por.csv` trong `data/raw/`. Script `scripts/build_dataset.py` chọn cột, bỏ trùng, mã hóa `yes/no` thành `1/0`, kiểm tra range và xuất dữ liệu sạch.

| Output | Ý nghĩa |
| --- | --- |
| `data/processed/student_performance_clean.csv` | Dữ liệu sạch |
| `reports/processing_audit.json` | Audit preprocessing |
| `reports/tables/pearson_correlation.csv` | Bảng Pearson |
| `reports/figures/pearson_heatmap.png` | Heatmap correlation |
| `reports/figures/hist_absences.png` | Histogram absences |
| `reports/figures/scatter_g2_g3.png` | Scatter G2-G3 |

## 6. Thiết kế mô hình dự đoán

Project có 3 scenario:

| Scenario | Required fields | Model artifact | UI mode | Status |
| --- | --- | --- | --- | --- |
| `web_minimal` | `studytime`, `failures`, `absences`, `schoolsup`, `famsup`, `internet` | `model_web_minimal.joblib` | Dự đoán nhanh | Có artifact |
| `early_warning` | web_minimal + `subject`, `higher`, `traveltime` | `model_early_warning.joblib` | Cảnh báo sớm | Có artifact |
| `reference` | early_warning + `G1`, `G2` | `model_reference.joblib` | Tham chiếu có G1/G2 | Có artifact |

`web_minimal` là mặc định vì khớp form đơn giản. `early_warning` là hướng nâng cấp khuyến nghị vì chỉ thêm 3 field. `reference` thường chính xác hơn vì dùng thêm điểm quá trình `G1/G2`.

## 7. Thiết kế hệ thống

Luồng chính: Browser gửi form đến ASP.NET Core MVC, MVC gọi FastAPI `/predict`, FastAPI chọn model theo scenario và trả điểm dự đoán, MVC lưu kết quả vào MySQL `PredictionHistory`.

Minh chứng:

- `reports/figures/architecture_diagram.mmd`
- `reports/figures/prediction_flow.mmd`
- `docs/system-design.md`

## 8. Xây dựng ứng dụng

Backend FastAPI có `/health`, `/model-info`, `/predict`. `/predict` hỗ trợ field `scenario`, mặc định là `web_minimal`. Frontend có nút **Nâng cấp mô hình dự đoán**, ẩn/hiện field theo scenario và hiển thị điểm thang 20, thang 10, scenario đã chọn. Database lưu thêm cột nullable `Scenario`. Hiện repository có đủ 3 artifact model trong `ml-service/artifacts/`.

## 9. Thực nghiệm và kết quả

Model comparison hiện có trong `reports/tables/model_comparison.csv`. Các test backend nằm ở `ml-service/tests/test_predict_api.py`. Một số test nâng cao chấp nhận `503` nếu artifact `early_warning` hoặc `reference` chưa được train.

## 10. Kết luận và định hướng phát triển

Project đã có pipeline dữ liệu, mô hình hồi quy, API, frontend, lưu history và phần mở rộng chọn scenario. Hướng phát triển tiếp theo là train đủ artifact cho `early_warning` và `reference`, chụp screenshot demo, bổ sung phân công thành viên thật và hoàn thiện Word/PPT.

## 11. Tài liệu tham khảo

- UCI Student Performance dataset.
- FastAPI, Pydantic, scikit-learn, pandas, matplotlib.
- ASP.NET Core MVC, MySQL, MySqlConnector.

## 12. Phụ lục

| Nội dung | File |
| --- | --- |
| API spec | `docs/api-spec.md`, `docs/api/predict-api.md` |
| Database | `database/schema/001_init.sql`, `database/migrations/003_add_scenario.sql` |
| Manual tests | `tests/manual/test_cases.md` |
| Screenshot checklist | `docs/screenshots/README.md` |

Screenshot demo thật: **Need to capture manually**.
