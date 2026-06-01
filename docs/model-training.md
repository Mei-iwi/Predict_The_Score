# Huấn luyện và đánh giá mô hình

## Bài toán

Bài toán là hồi quy dự đoán điểm cuối kỳ `G3` trên thang 20. Model chính đang dùng là `LinearRegression` vì dễ giải thích, phù hợp đồ án sinh viên và có hệ số cho từng biến.

## Feature scenarios

| Scenario | Biến sử dụng | Mục đích |
| --- | --- | --- |
| `reference` | `subject`, `studytime`, `failures`, `absences`, `G1`, `G2`, `schoolsup`, `famsup`, `internet`, `higher`, `traveltime` | So sánh độ chính xác khi có nhiều thông tin |
| `early_warning` | Không dùng `G1/G2`, có thêm `subject`, `higher`, `traveltime` | Dự đoán sớm hơn trước khi có điểm kỳ |
| `web_minimal` | `studytime`, `failures`, `absences`, `schoolsup`, `famsup`, `internet` | Khớp đúng form web hiện tại |

## Quy trình train

Script chính: `scripts/train_model.py`

1. Đọc `data/processed/student_performance_clean.csv`.
2. Đọc `data/processed/feature_config.json`.
3. Chọn scenario, mặc định là `web_minimal`.
4. Chia train/test với `test_size=0.2`, `random_state=42`.
5. Train `LinearRegression`.
6. Lưu model bundle vào `ml-service/artifacts/model.joblib`.
7. Lưu metrics, coefficients, intercept và feature names vào `reports/tables/metrics_web_minimal.json`.

## Kết quả so sánh

Theo `reports/tables/model_comparison.csv`:

| Scenario | MAE | MSE | RMSE | R2 | Nhận xét |
| --- | ---: | ---: | ---: | ---: | --- |
| `reference` | 0.9185 | 2.5454 | 1.5954 | 0.7823 | Tốt nhất vì có `G1/G2` |
| `early_warning` | 2.3255 | 9.8658 | 3.1410 | 0.1563 | Dự đoán sớm, ít thông tin hơn |
| `web_minimal` | 2.3173 | 10.6394 | 3.2618 | 0.0902 | Phù hợp form web nhưng R2 thấp |

## Lý do giữ `web_minimal` cho ứng dụng

`reference` chính xác hơn nhưng yêu cầu các trường mà web form hiện tại chưa có. `web_minimal` dùng đúng 6 trường người dùng nhập được, nên phù hợp để demo ứng dụng end-to-end. Khi trình bày, cần nói rõ đây là đánh đổi giữa độ chính xác và mức đơn giản của form nhập liệu.

## Lệnh chạy

```bash
python scripts/build_dataset.py
python scripts/train_model.py --scenario web_minimal
python scripts/evaluate_model.py
python scripts/compare_models.py
```

