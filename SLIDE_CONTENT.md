# SLIDE_CONTENT.md

## Slide 1 - Tên đề tài
- Xây dựng ứng dụng để dự đoán điểm số của học sinh
- Môn Khai phá dữ liệu / Data Mining
- Nhóm: Need confirmation
- Evidence: `README.md`

## Slide 2 - Thành viên và phân công
- Điền tên thành viên thật
- Nêu nhiệm vụ từng người
- Evidence: `docs/teamwork.md`

## Slide 3 - Bài toán
- Dự đoán điểm cuối kỳ `G3`
- Bài toán hồi quy
- Output thang 20 và thang 10

## Slide 4 - Mục tiêu project
- Xử lý dữ liệu
- Train model
- Xây dựng FastAPI backend
- Xây dựng ASP.NET MVC frontend
- Lưu lịch sử dự đoán

## Slide 5 - Dataset overview
- UCI Student Performance
- `student-mat.csv`, `student-por.csv`
- Evidence: `data/raw/`, `reports/processing_audit.json`

## Slide 6 - Data preprocessing
- Chọn cột
- Bỏ trùng
- Mã hóa yes/no thành 1/0
- Kiểm tra range

## Slide 7 - Data analysis
- Pearson correlation
- Heatmap
- Histogram absences
- Scatter G2-G3
- Evidence: `reports/figures/`

## Slide 8 - Feature scenarios
- `web_minimal`
- `early_warning`
- `reference`
- Evidence: `data/processed/feature_config.json`

## Slide 9 - Regression model
- LinearRegression
- Target `G3`
- Metrics: MAE, MSE, RMSE, R2

## Slide 10 - Training process
- `build_dataset.py`
- `train_model.py --scenario ...`
- `evaluate_model.py`
- `compare_models.py`

## Slide 11 - Evaluation metrics
- Giải thích MAE, MSE, RMSE, R2
- Evidence: `reports/tables/model_comparison.csv`

## Slide 12 - Model comparison
- `reference` có nhiều thông tin nhất
- `web_minimal` phù hợp form đơn giản
- `early_warning` là hướng nâng cấp hợp lý

## Slide 13 - Advanced scenario extension
- Nút "Nâng cấp mô hình dự đoán"
- Chọn scenario
- Ẩn/hiện field theo scenario
- Repo hiện có đủ artifact cho `web_minimal`, `early_warning`, `reference`
- Evidence: `Views/Home/Index.cshtml`, `wwwroot/js/script.js`

## Slide 14 - System architecture
- Browser -> MVC -> FastAPI -> Model
- MVC -> MySQL
- Evidence: `reports/figures/architecture_diagram.mmd`

## Slide 15 - Prediction flow
- Submit form
- Validate
- Predict
- Save history
- Display result
- Evidence: `reports/figures/prediction_flow.mmd`

## Slide 16 - Backend FastAPI
- `/health`
- `/model-info`
- `/predict`
- Scenario-based model loading

## Slide 17 - Frontend MVC
- Form mặc định đơn giản
- Advanced mode ẩn mặc định
- Hiển thị score, scenario, history

## Slide 18 - Database and history
- `PredictionHistory`
- Lưu score thang 20/10, model, scenario, created time
- Evidence: `database/schema/001_init.sql`

## Slide 19 - Demo guide
- Chạy backend
- Chạy frontend
- Test web_minimal
- Test early_warning/reference nếu artifact tồn tại
- Mở Swagger

## Slide 20 - Kết quả và hướng phát triển
- Hoàn thiện pipeline và app end-to-end
- Cần chụp screenshot thủ công
- Cần xác nhận phân công nhóm
- Có đủ artifact model cho 3 scenario; có thể train lại nếu muốn cập nhật metrics
