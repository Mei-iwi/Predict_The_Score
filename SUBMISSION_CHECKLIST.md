# SUBMISSION_CHECKLIST.md

## 1. Source code checklist

- [x] Backend FastAPI có `/health`, `/model-info`, `/predict`
- [x] Frontend ASP.NET Core MVC có form dự đoán
- [x] Database schema có `PredictionHistory`
- [x] API `/predict` hỗ trợ `scenario`
- [x] `web_minimal` là mặc định
- [x] Advanced mode ẩn mặc định
- [x] Nút nâng cấp hiển thị selector scenario
- [x] History có cột `Scenario`
- [x] Có `model_early_warning.joblib`
- [x] Có `model_reference.joblib`
- [ ] Docker chạy end-to-end

## 2. Report checklist

- [x] Có đủ nguồn nội dung 12 mục trong `REPORT_SOURCE_MATERIAL_UPDATED.md`
- [x] Có phần "Phần mở rộng: lựa chọn kịch bản dự đoán"
- [x] Có bảng scenario
- [x] Có evidence file paths
- [ ] Word report hoàn thiện
- [ ] Screenshot demo thật
- [ ] Teamwork evidence thật

## 3. Slide checklist

- [x] Có outline 20 slide trong `SLIDE_CONTENT.md`
- [x] Có slide scenario extension
- [x] Có slide architecture và prediction flow
- [ ] Tạo file PowerPoint `.pptx`
- [ ] Chèn screenshot demo

## 4. Demo checklist

- [ ] Mở webapp
- [ ] Test `web_minimal`
- [ ] Bấm upgrade button
- [ ] Test `early_warning` nếu model tồn tại
- [ ] Test `reference` nếu model tồn tại
- [ ] Show predicted score
- [ ] Show history with scenario
- [ ] Open Swagger `/docs`
- [ ] Show database history if possible

## 5. Missing confirmation checklist

- [ ] Team member contribution confirmation
- [ ] GitHub link confirmation
- [ ] Screenshot capture
- [ ] Final teacher/instructor info
- [ ] Real deployment URL if available
