# Phân tích dữ liệu

## Nguồn dữ liệu

Dữ liệu dùng trong project là **UCI Student Performance**. Project lưu hai file gốc tại:

- `data/raw/student-mat.csv`
- `data/raw/student-por.csv`

Script xử lý chính là `scripts/build_dataset.py`.

## Các bước tiền xử lý

| Bước | Mô tả | Output |
| --- | --- | --- |
| Đọc dữ liệu | Đọc hai file Toán và Bồ Đào Nha, thêm cột `subject` | DataFrame gộp |
| Chọn cột | Chọn các biến cần cho phân tích và mô hình | `selected_columns` trong audit |
| Bỏ trùng | Đếm và loại dòng trùng | `duplicate_rows` |
| Ép kiểu | Chuyển các cột số sang numeric | Kiểm tra missing sau cast |
| Mã hóa | `yes/no` được mã hóa thành `1/0` | Cột binary dùng được cho model |
| Kiểm tra miền giá trị | Giữ dữ liệu trong range hợp lệ | `invalid_rows_out_of_range.csv` nếu có |
| Xuất dữ liệu sạch | Lưu dataset sạch | `data/processed/student_performance_clean.csv` |

## Audit hiện tại

Theo `reports/processing_audit.json`:

| Chỉ số | Giá trị |
| --- | ---: |
| Số dòng ban đầu | 1044 |
| Số dòng sau chọn cột | 1044 |
| Số dòng trùng | 21 |
| Số dòng sau bỏ trùng | 1023 |
| Số dòng missing/invalid | 0 |
| Số dòng sạch cuối cùng | 1023 |

## Biểu đồ và bảng phân tích

| File | Ý nghĩa |
| --- | --- |
| `reports/tables/pearson_correlation.csv` | Bảng tương quan Pearson giữa các biến số |
| `reports/figures/pearson_heatmap.png` | Heatmap giúp nhìn nhanh biến nào liên quan mạnh đến `G3` |
| `reports/figures/hist_absences.png` | Phân bố số buổi vắng học |
| `reports/figures/scatter_g2_g3.png` | Quan hệ giữa điểm kỳ 2 `G2` và điểm cuối kỳ `G3` |

## Nhận xét dùng cho báo cáo

- `G2` thường có tương quan cao với `G3`, nên scenario `reference` dùng thêm `G1/G2` có kết quả tốt hơn.
- Scenario `web_minimal` không dùng `G1/G2` vì form web hiện tại chưa thu thập các điểm này. Vì vậy độ chính xác thấp hơn nhưng phù hợp ứng dụng demo.
- Việc mã hóa `yes/no` thành `1/0` giúp các biến hỗ trợ học tập và internet có thể đưa trực tiếp vào mô hình hồi quy tuyến tính.

