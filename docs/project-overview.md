# Tổng quan project

## Mục tiêu

Project **Predict The Score** xây dựng một ứng dụng dự đoán điểm cuối kỳ `G3` của học sinh. Bài toán hiện tại là hồi quy, dùng mô hình `LinearRegression` để dự đoán điểm trên thang 20 và quy đổi thêm sang thang 10 cho giao diện.

## Phạm vi

- Dữ liệu: UCI Student Performance gồm `student-mat.csv` và `student-por.csv`.
- Input web hiện tại: `studytime`, `failures`, `absences`, `schoolsup`, `famsup`, `internet`.
- Output: `predicted_score`, `predicted_score_10`, `model_name`, `message`.
- Lưu lịch sử dự đoán vào bảng MySQL `PredictionHistory`.

## Thành phần hệ thống

| Thành phần | Công nghệ | Vai trò |
| --- | --- | --- |
| Data scripts | Python, pandas, matplotlib | Làm sạch dữ liệu, audit, biểu đồ, train/evaluate model |
| ML backend | FastAPI, Pydantic, scikit-learn | Nhận request, validate input, gọi model, trả kết quả |
| Web frontend | ASP.NET Core MVC, Razor, JavaScript | Form nhập liệu, gọi backend MVC, hiển thị kết quả và lịch sử |
| Database | MySQL | Lưu lịch sử dự đoán |

## Luồng dự đoán

1. Người dùng nhập thông tin học sinh trên giao diện web.
2. JavaScript gửi JSON đến `/Predict/Submit`.
3. MVC controller kiểm tra model state, gọi FastAPI `/predict`.
4. FastAPI nạp model, tạo dataframe theo feature list, dự đoán điểm `G3`.
5. Điểm được giới hạn trong khoảng 0-20 và quy đổi sang thang 10.
6. MVC lưu lịch sử vào MySQL và trả kết quả về trình duyệt.

