# REPORT_SOURCE_MATERIAL.md

Tài liệu này là nguồn nội dung để đưa vào ChatGPT Web viết báo cáo Word tiếng Việt cho đề tài: **"Xây dựng ứng dụng để dự đoán điểm số của học sinh"** trong học phần **Khai phá dữ liệu / Data Mining**. Nội dung dưới đây chỉ dựa trên các file và kết quả hiện có trong repository, không tự thêm chức năng hoặc kết quả ngoài project.

## 0. Tổng quan project đã kiểm tra

- Tên repository: `Predict_The_Score`, remote GitHub `https://github.com/Mei-iwi/Predict_The_Score.git`. Minh chứng: lệnh `git remote -v`.
- Branch hiện tại: `mainhatcuong`. Minh chứng: lệnh `git branch -a --show-current`.
- Mục tiêu chính: xây dựng hệ thống dự đoán điểm số cuối kỳ `G3` của học sinh dựa trên một số thông tin học tập và hỗ trợ học tập. Minh chứng: [README.md](README.md), [docs/architecture/architecture-overview.md](docs/architecture/architecture-overview.md), [scripts/train_model.py](scripts/train_model.py), [ml-service/app/main.py](ml-service/app/main.py).
- Bài toán khai phá dữ liệu: bài toán hồi quy, dự đoán biến mục tiêu `G3` trong thang điểm 0-20. Minh chứng: [data/processed/feature_config.json](data/processed/feature_config.json), [scripts/train_model.py](scripts/train_model.py), [ml-service/app/services/predictor.py](ml-service/app/services/predictor.py).
- Công nghệ chính được dùng: Python, pandas, scikit-learn, matplotlib, joblib, FastAPI, Pydantic, Uvicorn, ASP.NET Core MVC, Razor View, JavaScript, CSS, MySQL, Docker Compose. Minh chứng: [ml-service/requirements.txt](ml-service/requirements.txt), [webapp/PredictTheScore.Web/PredictTheScore.Web.csproj](webapp/PredictTheScore.Web/PredictTheScore.Web.csproj), [docker-compose.yml](docker-compose.yml).
- Các thư mục/file quan trọng:
  - `scripts/`: xử lý dữ liệu, huấn luyện, đánh giá, so sánh mô hình. Minh chứng: [scripts/build_dataset.py](scripts/build_dataset.py), [scripts/train_model.py](scripts/train_model.py), [scripts/evaluate_model.py](scripts/evaluate_model.py), [scripts/compare_models.py](scripts/compare_models.py).
  - `ml-service/`: backend FastAPI. Minh chứng: [ml-service/app/main.py](ml-service/app/main.py).
  - `webapp/PredictTheScore.Web/`: frontend ASP.NET Core MVC. Minh chứng: [webapp/PredictTheScore.Web/Program.cs](webapp/PredictTheScore.Web/Program.cs), [webapp/PredictTheScore.Web/Views/Home/Index.cshtml](webapp/PredictTheScore.Web/Views/Home/Index.cshtml).
  - `database/`: schema và migration MySQL. Minh chứng: [database/schema/001_init.sql](database/schema/001_init.sql), [database/migrations/002_add_predicted_score_10.sql](database/migrations/002_add_predicted_score_10.sql).
  - `reports/`: bảng, biểu đồ, audit phục vụ báo cáo. Minh chứng: [reports/processing_audit.json](reports/processing_audit.json), [reports/tables/model_comparison.csv](reports/tables/model_comparison.csv).
- Chức năng đã thực hiện:
  - Tải và xử lý dữ liệu UCI Student Performance. Minh chứng: [scripts/download_data.py](scripts/download_data.py), [scripts/build_dataset.py](scripts/build_dataset.py), [data/raw/student-mat.csv](data/raw/student-mat.csv), [data/raw/student-por.csv](data/raw/student-por.csv).
  - Sinh dữ liệu sạch, audit, bảng Pearson và biểu đồ. Minh chứng: [data/processed/student_performance_clean.csv](data/processed/student_performance_clean.csv), [reports/processing_audit.json](reports/processing_audit.json), [reports/tables/pearson_correlation.csv](reports/tables/pearson_correlation.csv), [reports/figures/pearson_heatmap.png](reports/figures/pearson_heatmap.png).
  - Huấn luyện `LinearRegression` và lưu model. Minh chứng: [scripts/train_model.py](scripts/train_model.py), `ml-service/artifacts/model.joblib`.
  - So sánh các kịch bản đặc trưng. Minh chứng: [scripts/compare_models.py](scripts/compare_models.py), [reports/tables/model_comparison.csv](reports/tables/model_comparison.csv).
  - Backend API `/predict`, `/health`, `/model-info`. Minh chứng: [ml-service/app/main.py](ml-service/app/main.py).
  - Frontend nhập dữ liệu, gọi API, hiển thị điểm thang 20 và thang 10, xem lịch sử. Minh chứng: [webapp/PredictTheScore.Web/Views/Home/Index.cshtml](webapp/PredictTheScore.Web/Views/Home/Index.cshtml), [webapp/PredictTheScore.Web/wwwroot/js/script.js](webapp/PredictTheScore.Web/wwwroot/js/script.js), [webapp/PredictTheScore.Web/Controllers/PredictController.cs](webapp/PredictTheScore.Web/Controllers/PredictController.cs).
  - Lưu lịch sử dự đoán vào MySQL. Minh chứng: [webapp/PredictTheScore.Web/Services/PredictionHistoryService.cs](webapp/PredictTheScore.Web/Services/PredictionHistoryService.cs), [database/schema/001_init.sql](database/schema/001_init.sql).
  - Kiểm thử backend API. Minh chứng: [ml-service/tests/test_predict_api.py](ml-service/tests/test_predict_api.py).
- Chức năng chưa thấy hoặc cần xác nhận:
  - Danh sách thành viên nhóm và phân công cá nhân: **Need confirmation**. Các file `docs/progress/week-01.md`, `week-02.md`, `week-03.md` đang để `TBD`.
  - Ảnh chụp giao diện demo thật: **Not found in the current project**.
  - Issue/task tracker chi tiết: **Not found in the current project**.
  - Kiểm thử tự động cho frontend MVC: **Not found in the current project**.

## 1. Lịch làm việc nhóm theo tuần

Git history có một số commit mô tả tiến trình nhưng chưa đủ để xác định chính xác từng thành viên. Các commit gần nhất gồm: `first commit`, `Add docker file scripts`, `connect backend fontend`, `add model predict and model_loader`, `connect dataabase mysql on docker`, `feat: improve prediction app, model reports, API docs, and tests`, `fix error`. Minh chứng: lệnh `git log --oneline --all --decorate -n 30`.

| Tuần | Nội dung công việc | Thành viên/phần phụ trách nếu xác định được | Kết quả đạt được | Minh chứng trong project |
| --- | --- | --- | --- | --- |
| Tuần 1 | Khởi tạo cấu trúc project, xác định đề tài, chuẩn bị dữ liệu Student Performance | Need confirmation | Có cấu trúc `data`, `scripts`, `ml-service`, `webapp`, `database`, `docs` | [README.md](README.md), [docs/progress/week-01.md](docs/progress/week-01.md), commit `8cea60b first commit` |
| Tuần 2 | Xử lý dữ liệu, tạo dataset sạch, cấu hình feature, bắt đầu mô hình dự đoán | Need confirmation | Có `build_dataset.py`, `student_performance_clean.csv`, `feature_config.json` | [scripts/build_dataset.py](scripts/build_dataset.py), [data/processed/feature_config.json](data/processed/feature_config.json), [docs/progress/week-01.md](docs/progress/week-01.md) |
| Tuần 3 | Xây dựng backend FastAPI, nạp model, tạo endpoint dự đoán | Need confirmation | Có API `/predict`, service nạp model và xử lý input | [ml-service/app/main.py](ml-service/app/main.py), [ml-service/app/services/model_loader.py](ml-service/app/services/model_loader.py), commit `0e6dbe3 add model predict and model_loader` |
| Tuần 4 | Xây dựng frontend ASP.NET Core MVC, kết nối frontend với backend | Need confirmation | Có form nhập dữ liệu, JS gọi `/Predict/Submit`, client gọi FastAPI | [webapp/PredictTheScore.Web/Views/Home/Index.cshtml](webapp/PredictTheScore.Web/Views/Home/Index.cshtml), [webapp/PredictTheScore.Web/wwwroot/js/script.js](webapp/PredictTheScore.Web/wwwroot/js/script.js), [webapp/PredictTheScore.Web/Services/MlApiClient.cs](webapp/PredictTheScore.Web/Services/MlApiClient.cs), commit `aea6cf3 connect backend fontend` |
| Tuần 5 | Tích hợp MySQL, lưu lịch sử dự đoán, Docker hóa | Need confirmation | Có bảng `PredictionHistory`, Docker Compose gồm MySQL, ML service, webapp | [database/schema/001_init.sql](database/schema/001_init.sql), [docker-compose.yml](docker-compose.yml), [webapp/PredictTheScore.Web/Services/PredictionHistoryService.cs](webapp/PredictTheScore.Web/Services/PredictionHistoryService.cs), commit `1baf162 connect dataabase mysql on docker` |
| Tuần 6 | Bổ sung audit, biểu đồ, model comparison, API docs, test cases | Need confirmation | Có audit JSON, biểu đồ, bảng model comparison, test backend | [reports/processing_audit.json](reports/processing_audit.json), [reports/tables/model_comparison.csv](reports/tables/model_comparison.csv), [ml-service/tests/test_predict_api.py](ml-service/tests/test_predict_api.py), commit `3acd39d feat: improve prediction app, model reports, API docs, and tests` |

Ghi chú: Lịch trên là gợi ý dựa trên file hiện có và git history; phân công thành viên cụ thể cần nhóm xác nhận.

## 2. Phân công công việc thành viên

Không tìm thấy danh sách thành viên chính thức trong repository. Branch hiện tại là `mainhatcuong`, một số commit/branch có tên `mainhatcuong`, nhưng repository không đủ bằng chứng để xác nhận đây là thành viên nào hoặc toàn bộ nhóm gồm những ai. Vì vậy, bảng dưới đây chỉ ghi các vai trò cần có và đánh dấu **Need confirmation**.

| STT | Thành viên | Vai trò | Công việc phụ trách | Minh chứng file/commit | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| 1 | Need confirmation | Phân tích dữ liệu | Tải dữ liệu, làm sạch, tạo audit, biểu đồ Pearson | [scripts/download_data.py](scripts/download_data.py), [scripts/build_dataset.py](scripts/build_dataset.py), [reports/processing_audit.json](reports/processing_audit.json) | Cần xác nhận người phụ trách |
| 2 | Need confirmation | Machine Learning | Huấn luyện LinearRegression, đánh giá, so sánh kịch bản | [scripts/train_model.py](scripts/train_model.py), [scripts/evaluate_model.py](scripts/evaluate_model.py), [scripts/compare_models.py](scripts/compare_models.py) | Cần xác nhận người phụ trách |
| 3 | Need confirmation | Backend | Xây dựng FastAPI, schema request/response, nạp model | [ml-service/app/main.py](ml-service/app/main.py), [ml-service/app/schemas/request.py](ml-service/app/schemas/request.py), [ml-service/app/services/predictor.py](ml-service/app/services/predictor.py) | Cần xác nhận người phụ trách |
| 4 | Need confirmation | Frontend | Xây dựng form, gọi API, hiển thị kết quả và lịch sử | [webapp/PredictTheScore.Web/Views/Home/Index.cshtml](webapp/PredictTheScore.Web/Views/Home/Index.cshtml), [webapp/PredictTheScore.Web/wwwroot/js/script.js](webapp/PredictTheScore.Web/wwwroot/js/script.js), [webapp/PredictTheScore.Web/Controllers/PredictController.cs](webapp/PredictTheScore.Web/Controllers/PredictController.cs) | Cần xác nhận người phụ trách |
| 5 | Need confirmation | Database/DevOps/Test | MySQL schema, Docker Compose, test API | [database/schema/001_init.sql](database/schema/001_init.sql), [docker-compose.yml](docker-compose.yml), [ml-service/tests/test_predict_api.py](ml-service/tests/test_predict_api.py) | Cần xác nhận người phụ trách |

## 3. Giới thiệu đề tài

### 3.1. Lý do chọn đề tài

Đề tài tập trung vào việc dự đoán điểm số cuối kỳ của học sinh dựa trên dữ liệu học tập và điều kiện hỗ trợ học tập. Đây là một bài toán phù hợp với học phần Khai phá dữ liệu vì có đầy đủ các bước: thu thập dữ liệu, tiền xử lý, phân tích tương quan, huấn luyện mô hình hồi quy, đánh giá mô hình và triển khai dự đoán qua ứng dụng web. Dữ liệu sử dụng là bộ UCI Student Performance, được lưu trong [data/raw/student-mat.csv](data/raw/student-mat.csv) và [data/raw/student-por.csv](data/raw/student-por.csv).

### 3.2. Sự cần thiết của đề tài

Trong môi trường giáo dục, việc dự báo sớm kết quả học tập giúp giáo viên hoặc người quản lý có thêm thông tin tham khảo để hỗ trợ học sinh. Project hiện tại không thay thế việc đánh giá của giáo viên, nhưng cung cấp một công cụ minh họa cách dùng dữ liệu học tập để dự đoán điểm `G3`. Minh chứng về biến mục tiêu `G3` và các kịch bản đặc trưng nằm trong [data/processed/feature_config.json](data/processed/feature_config.json).

### 3.3. Mục tiêu đề tài

Mục tiêu của project là xây dựng một ứng dụng có thể nhận dữ liệu đầu vào từ người dùng, gửi dữ liệu đến backend ML, trả về điểm dự đoán trên thang 20 và thang 10, đồng thời lưu lịch sử dự đoán. Minh chứng: [ml-service/app/main.py](ml-service/app/main.py), [webapp/PredictTheScore.Web/Controllers/PredictController.cs](webapp/PredictTheScore.Web/Controllers/PredictController.cs), [database/schema/001_init.sql](database/schema/001_init.sql).

### 3.4. Phạm vi đồ án

Phạm vi đồ án gồm dữ liệu UCI Student Performance, mô hình hồi quy tuyến tính `LinearRegression`, backend FastAPI, frontend ASP.NET Core MVC và MySQL lưu lịch sử. Project hiện chưa thấy chức năng đăng nhập người dùng, phân quyền, quản lý lớp/học sinh đầy đủ hoặc dashboard thống kê nâng cao. Các phần này đánh dấu **Not found in the current project**.

### 3.5. Đối tượng sử dụng hệ thống

Đối tượng sử dụng có thể là giáo viên, sinh viên thực hiện đồ án hoặc người muốn thử nghiệm mô hình dự đoán điểm số. Giao diện web cho phép nhập họ tên, lớp, thời gian tự học, số lần chưa đạt, số buổi vắng và các biến hỗ trợ học tập. Minh chứng: [webapp/PredictTheScore.Web/Views/Home/Index.cshtml](webapp/PredictTheScore.Web/Views/Home/Index.cshtml).

### 3.6. Kết quả dự kiến

Kết quả dự kiến là một hệ thống web có thể chạy cục bộ hoặc bằng Docker, dự đoán điểm `G3`, hiển thị kết quả thang 20 và thang 10, lưu lịch sử dự đoán, đồng thời có các file báo cáo dữ liệu và đánh giá mô hình. Minh chứng: [docker-compose.yml](docker-compose.yml), [reports/tables/metrics_web_minimal.json](reports/tables/metrics_web_minimal.json), [reports/figures/actual_vs_predicted_web_minimal.png](reports/figures/actual_vs_predicted_web_minimal.png).

## 4. Cơ sở lý thuyết

### 4.1. Tổng quan về khai thác dữ liệu

Khai thác dữ liệu là quá trình tìm ra tri thức, mẫu quan hệ hoặc quy luật có ích từ dữ liệu. Trong project này, khai thác dữ liệu được thể hiện qua việc phân tích bộ dữ liệu Student Performance, chọn biến đầu vào, làm sạch dữ liệu, tính tương quan Pearson, huấn luyện mô hình hồi quy và đánh giá bằng các độ đo sai số. Minh chứng triển khai: [scripts/build_dataset.py](scripts/build_dataset.py), [scripts/train_model.py](scripts/train_model.py), [scripts/evaluate_model.py](scripts/evaluate_model.py).

### 4.2. Quy trình khai thác dữ liệu

Quy trình trong project gồm: tải dữ liệu, chọn cột, mã hóa dữ liệu yes/no, kiểm tra trùng lặp và miền giá trị, sinh dữ liệu sạch, chia train/test, huấn luyện mô hình, đánh giá, lưu model và tích hợp API. Minh chứng: [scripts/download_data.py](scripts/download_data.py), [scripts/build_dataset.py](scripts/build_dataset.py), [scripts/train_model.py](scripts/train_model.py).

### 4.3. Bài toán hồi quy trong khai thác dữ liệu

Bài toán hồi quy dự đoán một giá trị số liên tục. Ở đây, biến cần dự đoán là `G3`, điểm cuối kỳ của học sinh trên thang 0-20. Mô hình nhận các biến đầu vào như `studytime`, `failures`, `absences`, `schoolsup`, `famsup`, `internet` trong kịch bản `web_minimal`. Minh chứng: [data/processed/feature_config.json](data/processed/feature_config.json).

### 4.4. Hồi quy tuyến tính

Hồi quy tuyến tính mô hình hóa quan hệ giữa biến mục tiêu và các biến đầu vào bằng tổ hợp tuyến tính của các hệ số. Project dùng `LinearRegression` từ scikit-learn. Minh chứng: [scripts/train_model.py](scripts/train_model.py), [scripts/compare_models.py](scripts/compare_models.py).

### 4.5. Phân tích tương quan Pearson

Tương quan Pearson đo mức độ quan hệ tuyến tính giữa hai biến số. Project tính ma trận Pearson cho các cột đã xử lý và lưu ra file CSV, đồng thời tạo heatmap. Minh chứng: [reports/tables/pearson_correlation.csv](reports/tables/pearson_correlation.csv), [reports/figures/pearson_heatmap.png](reports/figures/pearson_heatmap.png), [scripts/build_dataset.py](scripts/build_dataset.py).

### 4.6. Các độ đo đánh giá mô hình: MAE, MSE, RMSE, R²

Project sử dụng MAE, MSE, RMSE và R². MAE đo sai số tuyệt đối trung bình; MSE đo bình phương sai số trung bình; RMSE là căn bậc hai của MSE; R² thể hiện mức độ giải thích phương sai của mô hình. Minh chứng: [scripts/train_model.py](scripts/train_model.py), [scripts/evaluate_model.py](scripts/evaluate_model.py), [reports/tables/metrics_web_minimal.json](reports/tables/metrics_web_minimal.json).

### 4.7. Train/Test Split

Dữ liệu được chia thành tập train và test với `test_size = 0.2`, `random_state = 42`. Minh chứng: [scripts/train_model.py](scripts/train_model.py), [reports/tables/metrics_web_minimal.json](reports/tables/metrics_web_minimal.json), [reports/tables/model_comparison.json](reports/tables/model_comparison.json).

### 4.8. Công nghệ sử dụng

| Nhóm công nghệ | Công nghệ | Vai trò trong đồ án | File minh chứng |
| --- | --- | --- | --- |
| Ngôn ngữ/backend ML | Python | Xử lý dữ liệu, huấn luyện model, xây dựng API | [ml-service/requirements.txt](ml-service/requirements.txt), [scripts/train_model.py](scripts/train_model.py) |
| Web API | FastAPI | Cung cấp `/predict`, `/health`, `/model-info` | [ml-service/app/main.py](ml-service/app/main.py) |
| Schema validation | Pydantic | Kiểm tra input API | [ml-service/app/schemas/request.py](ml-service/app/schemas/request.py) |
| ML | scikit-learn | `LinearRegression`, train/test split, metrics | [scripts/train_model.py](scripts/train_model.py) |
| Data processing | pandas | Đọc CSV, xử lý dataframe, xuất CSV | [scripts/build_dataset.py](scripts/build_dataset.py) |
| Biểu đồ | matplotlib | Sinh heatmap, histogram, scatter, actual-vs-predicted | [scripts/build_dataset.py](scripts/build_dataset.py), [scripts/evaluate_model.py](scripts/evaluate_model.py) |
| Lưu model | joblib | Lưu và nạp model `.joblib` | [scripts/train_model.py](scripts/train_model.py), [ml-service/app/services/model_loader.py](ml-service/app/services/model_loader.py) |
| Frontend web | ASP.NET Core MVC / Razor | Giao diện nhập liệu và hiển thị kết quả | [webapp/PredictTheScore.Web/PredictTheScore.Web.csproj](webapp/PredictTheScore.Web/PredictTheScore.Web.csproj), [webapp/PredictTheScore.Web/Views/Home/Index.cshtml](webapp/PredictTheScore.Web/Views/Home/Index.cshtml) |
| Frontend interaction | JavaScript | Validate form, gọi `/Predict/Submit`, tải lịch sử | [webapp/PredictTheScore.Web/wwwroot/js/script.js](webapp/PredictTheScore.Web/wwwroot/js/script.js) |
| Database | MySQL | Lưu lịch sử dự đoán | [database/schema/001_init.sql](database/schema/001_init.sql), [docker-compose.yml](docker-compose.yml) |
| DB connector | MySqlConnector | ASP.NET Core truy vấn MySQL bằng raw SQL | [webapp/PredictTheScore.Web/PredictTheScore.Web.csproj](webapp/PredictTheScore.Web/PredictTheScore.Web.csproj), [webapp/PredictTheScore.Web/Services/PredictionHistoryService.cs](webapp/PredictTheScore.Web/Services/PredictionHistoryService.cs) |
| Container | Docker Compose | Chạy MySQL, ML service, webapp | [docker-compose.yml](docker-compose.yml) |

## 5. Phân tích dữ liệu

### 5.1. Nguồn dữ liệu

Project sử dụng bộ dữ liệu UCI Student Performance. Dữ liệu thô hiện có gồm [data/raw/student-mat.csv](data/raw/student-mat.csv), [data/raw/student-por.csv](data/raw/student-por.csv), [data/raw/student.txt](data/raw/student.txt) và [data/raw/student.zip](data/raw/student.zip). Script tải dữ liệu là [scripts/download_data.py](scripts/download_data.py). Citation chính thức của dataset trong báo cáo cần xác nhận thêm từ `student.txt` hoặc nguồn UCI: **Need confirmation**.

### 5.2. Mô tả bộ dữ liệu Student Performance

Hai file `student-mat.csv` và `student-por.csv` tương ứng dữ liệu học sinh của hai môn. Script xử lý thêm cột `subject` để phân biệt `mat` và `por`, sau đó gộp dữ liệu. Số dòng thô kiểm tra được: `student-mat.csv` có 395 dòng, `student-por.csv` có 649 dòng, tổng 1044 dòng. Minh chứng: lệnh `Import-Csv ... | Measure-Object`, [reports/processing_audit.json](reports/processing_audit.json).

### 5.3. Các thuộc tính đầu vào

Các cột được chọn gồm: `studytime`, `failures`, `absences`, `G1`, `G2`, `schoolsup`, `famsup`, `internet`, `higher`, `traveltime`, `G3`, `subject`. Minh chứng: [scripts/build_dataset.py](scripts/build_dataset.py), [reports/processing_audit.json](reports/processing_audit.json). Trong giao diện web hiện tại, các biến đầu vào gửi sang model `web_minimal` gồm `studytime`, `failures`, `absences`, `schoolsup`, `famsup`, `internet`. Minh chứng: [data/processed/feature_config.json](data/processed/feature_config.json), [webapp/PredictTheScore.Web/Models/PredictionRequestDto.cs](webapp/PredictTheScore.Web/Models/PredictionRequestDto.cs).

### 5.4. Thuộc tính mục tiêu cần dự đoán

Biến mục tiêu là `G3`, điểm cuối kỳ của học sinh trên thang 0-20. Minh chứng: [data/processed/feature_config.json](data/processed/feature_config.json), [scripts/train_model.py](scripts/train_model.py).

### 5.5. Mô tả dữ liệu thô

Dữ liệu thô được đọc bằng `pd.read_csv(..., sep=";")`. Các file nguồn được tìm trong `data/raw`, `student_performance/`, project root hoặc trong file zip. Minh chứng: [scripts/build_dataset.py](scripts/build_dataset.py). Sau khi gộp, dữ liệu có 1044 dòng ban đầu. Minh chứng: [reports/processing_audit.json](reports/processing_audit.json).

### 5.6. Kiểm tra dữ liệu thiếu, dữ liệu trùng, dữ liệu sai miền giá trị

Audit hiện tại ghi nhận:

| Nội dung kiểm tra | Kết quả | File minh chứng |
| --- | ---: | --- |
| Số dòng gốc | 1044 | [reports/processing_audit.json](reports/processing_audit.json) |
| Số dòng sau chọn cột | 1044 | [reports/processing_audit.json](reports/processing_audit.json) |
| Số dòng trùng | 21 | [reports/processing_audit.json](reports/processing_audit.json) |
| Số dòng sau bỏ trùng | 1023 | [reports/processing_audit.json](reports/processing_audit.json) |
| Dòng thiếu/không hợp lệ | 0 | [reports/processing_audit.json](reports/processing_audit.json) |
| Dòng sau làm sạch | 1023 | [reports/processing_audit.json](reports/processing_audit.json) |

Miền giá trị kiểm tra trong code gồm `studytime` 1-4, `failures` 0-4, `absences` 0-93, `G1/G2/G3` 0-20, `traveltime` 1-4. Minh chứng: [scripts/build_dataset.py](scripts/build_dataset.py).

### 5.7. Mã hóa dữ liệu dạng yes/no

Các cột `schoolsup`, `famsup`, `internet`, `higher` được mã hóa `yes` thành 1 và `no` thành 0. Minh chứng: [scripts/build_dataset.py](scripts/build_dataset.py), [reports/processing_audit.json](reports/processing_audit.json).

### 5.8. Làm sạch dữ liệu

Quy trình làm sạch gồm chọn cột, bỏ dòng trùng, ép kiểu numeric, mã hóa yes/no, mã hóa `subject` từ `mat/por` thành `0/1`, bỏ dòng có `NaN`, kiểm tra miền giá trị hợp lệ và lưu dữ liệu sạch ra [data/processed/student_performance_clean.csv](data/processed/student_performance_clean.csv). Minh chứng: [scripts/build_dataset.py](scripts/build_dataset.py).

### 5.9. Phân tích tương quan giữa các thuộc tính

Project tính Pearson correlation cho các cột đã xử lý và lưu tại [reports/tables/pearson_correlation.csv](reports/tables/pearson_correlation.csv). Hình heatmap nằm ở [reports/figures/pearson_heatmap.png](reports/figures/pearson_heatmap.png). Ngoài ra còn có histogram số buổi vắng [reports/figures/hist_absences.png](reports/figures/hist_absences.png) và scatter giữa `G2` và `G3` [reports/figures/scatter_g2_g3.png](reports/figures/scatter_g2_g3.png).

### 5.10. Nhận xét dữ liệu sau tiền xử lý

Dữ liệu sau tiền xử lý có 1023 dòng, đã loại 21 dòng trùng và không còn dòng thiếu/invalid theo audit hiện tại. Các biến dạng nhị phân đã được mã hóa số để đưa vào mô hình. Bộ dữ liệu sạch có thể dùng cho cả kịch bản tham chiếu có `G1/G2`, kịch bản cảnh báo sớm không dùng `G1/G2`, và kịch bản web tối giản chỉ dùng các trường có trên form. Minh chứng: [reports/processing_audit.json](reports/processing_audit.json), [data/processed/feature_config.json](data/processed/feature_config.json).

Các bảng/hình nên đưa vào báo cáo: `processing_audit.json`, `pearson_correlation.csv`, `pearson_heatmap.png`, `hist_absences.png`, `scatter_g2_g3.png`.

## 6. Thiết kế mô hình dự đoán

### 6.1. Xác định bài toán dự đoán điểm số

Project dự đoán điểm cuối kỳ `G3` của học sinh. Vì `G3` là điểm số liên tục trong khoảng 0-20, bài toán được mô hình hóa như bài toán hồi quy. Minh chứng: [scripts/train_model.py](scripts/train_model.py), [ml-service/app/services/predictor.py](ml-service/app/services/predictor.py).

### 6.2. Lựa chọn biến đầu vào

File [data/processed/feature_config.json](data/processed/feature_config.json) định nghĩa ba kịch bản:

- `reference`: `subject`, `studytime`, `failures`, `absences`, `G1`, `G2`, `schoolsup`, `famsup`, `internet`, `higher`, `traveltime`.
- `early_warning`: `subject`, `studytime`, `failures`, `absences`, `schoolsup`, `famsup`, `internet`, `higher`, `traveltime`.
- `web_minimal`: `studytime`, `failures`, `absences`, `schoolsup`, `famsup`, `internet`.

### 6.3. Lựa chọn mô hình hồi quy

Mô hình được dùng là `LinearRegression` từ scikit-learn. Minh chứng: [scripts/train_model.py](scripts/train_model.py), [scripts/compare_models.py](scripts/compare_models.py). Không thấy mô hình Decision Tree hoặc mô hình khác được dùng trong bản hiện tại: **Not found in the current project**.

### 6.4. Quy trình huấn luyện mô hình

Script [scripts/train_model.py](scripts/train_model.py) đọc dữ liệu sạch và `feature_config.json`, chọn scenario, chia train/test với `test_size=0.2`, `random_state=42`, huấn luyện `LinearRegression`, tính metrics train/test, lưu bundle model và metrics. Model mặc định được lưu tại `ml-service/artifacts/model.joblib`, model theo scenario tại `ml-service/artifacts/model_web_minimal.joblib`.

### 6.5. Kịch bản thử nghiệm: reference, early_warning, web_minimal

Script [scripts/compare_models.py](scripts/compare_models.py) so sánh ba kịch bản đặc trưng với cùng mô hình `LinearRegression`. Kịch bản `reference` có nhiều biến nhất và dùng cả `G1`, `G2`; `early_warning` bỏ `G1`, `G2`; `web_minimal` phù hợp giao diện hiện tại vì chỉ dùng 6 trường trên form.

### 6.6. Đánh giá mô hình

Metrics `web_minimal` sau train/test:

| Tập dữ liệu | MAE | MSE | RMSE | R² | File minh chứng |
| --- | ---: | ---: | ---: | ---: | --- |
| Train | 2.6579 | 13.0749 | 3.6159 | 0.1822 | [reports/tables/metrics_web_minimal.json](reports/tables/metrics_web_minimal.json) |
| Test | 2.3173 | 10.6394 | 3.2618 | 0.0902 | [reports/tables/metrics_web_minimal.json](reports/tables/metrics_web_minimal.json), [reports/tables/evaluation_web_minimal.json](reports/tables/evaluation_web_minimal.json) |

### 6.7. So sánh kết quả và chọn mô hình dùng cho ứng dụng

| Kịch bản | Số biến | MAE | MSE | RMSE | R² | File minh chứng |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| reference | 11 | 0.9185 | 2.5454 | 1.5954 | 0.7823 | [reports/tables/model_comparison.csv](reports/tables/model_comparison.csv) |
| early_warning | 9 | 2.3255 | 9.8661 | 3.1410 | 0.1563 | [reports/tables/model_comparison.csv](reports/tables/model_comparison.csv) |
| web_minimal | 6 | 2.3173 | 10.6394 | 3.2618 | 0.0902 | [reports/tables/model_comparison.csv](reports/tables/model_comparison.csv) |

Theo RMSE, `reference` tốt nhất vì có thêm `G1` và `G2`, đây là hai điểm quá trình gần với điểm cuối kỳ. Tuy nhiên, ứng dụng web hiện tại dùng `web_minimal` vì form chỉ thu thập 6 trường đơn giản. Đây là một đánh đổi giữa độ chính xác và tính đơn giản khi nhập liệu. Minh chứng: [data/processed/feature_config.json](data/processed/feature_config.json), [webapp/PredictTheScore.Web/Views/Home/Index.cshtml](webapp/PredictTheScore.Web/Views/Home/Index.cshtml).

### 6.8. Lưu mô hình và tích hợp vào backend

Model bundle lưu bằng joblib, gồm model, scenario, feature names, target, metrics, coefficients, intercept, train/test indices. Minh chứng: [scripts/train_model.py](scripts/train_model.py). Backend nạp model từ `ml-service/artifacts/model.joblib`. Minh chứng: [ml-service/app/services/model_loader.py](ml-service/app/services/model_loader.py). Khi dự đoán, backend clip điểm trong khoảng 0-20. Minh chứng: [ml-service/app/services/predictor.py](ml-service/app/services/predictor.py).

Hạn chế thực tế: `web_minimal` có R² test khoảng 0.0902, tức khả năng giải thích biến thiên điểm còn thấp so với `reference`. Điều này cần nêu rõ trong báo cáo để tránh phóng đại chất lượng mô hình.

## 7. Thiết kế hệ thống

### 7.1. Kiến trúc tổng thể hệ thống

Hệ thống gồm ba phần chính: frontend ASP.NET Core MVC, backend FastAPI ML service và database MySQL. Frontend nhận input, gọi backend qua HTTP, backend dùng model đã train để dự đoán, frontend lưu lịch sử vào MySQL. Minh chứng: [docs/architecture/architecture-overview.md](docs/architecture/architecture-overview.md), [docker-compose.yml](docker-compose.yml).

### 7.2. Sơ đồ luồng xử lý dự đoán

Luồng xử lý: người dùng nhập form -> browser gửi JSON đến `POST /Predict/Submit` -> MVC controller tạo DTO -> `MlApiClient` gọi FastAPI `POST /predict` -> FastAPI validate input và dự đoán -> trả `predicted_score`, `predicted_score_10`, `model_name`, `message` -> MVC lưu lịch sử -> frontend hiển thị kết quả và reload lịch sử. Minh chứng: [webapp/PredictTheScore.Web/Controllers/PredictController.cs](webapp/PredictTheScore.Web/Controllers/PredictController.cs), [webapp/PredictTheScore.Web/Services/MlApiClient.cs](webapp/PredictTheScore.Web/Services/MlApiClient.cs), [ml-service/app/main.py](ml-service/app/main.py), [webapp/PredictTheScore.Web/wwwroot/js/script.js](webapp/PredictTheScore.Web/wwwroot/js/script.js).

### 7.3. Thiết kế backend FastAPI

Backend có các endpoint:

- `GET /`: kiểm tra API cơ bản.
- `GET /health`: trả trạng thái và model đã load hay chưa.
- `GET /model-info`: trả tên model/scenario, feature names, target, metrics.
- `POST /predict`: nhận input, dự đoán điểm.

Minh chứng: [ml-service/app/main.py](ml-service/app/main.py).

### 7.4. Thiết kế frontend ASP.NET Core MVC

Frontend dùng ASP.NET Core MVC, cấu hình DI cho `IPredictionHistoryService` và `IMlApiClient`. Minh chứng: [webapp/PredictTheScore.Web/Program.cs](webapp/PredictTheScore.Web/Program.cs). Giao diện chính nằm ở [webapp/PredictTheScore.Web/Views/Home/Index.cshtml](webapp/PredictTheScore.Web/Views/Home/Index.cshtml), JavaScript xử lý form ở [webapp/PredictTheScore.Web/wwwroot/js/script.js](webapp/PredictTheScore.Web/wwwroot/js/script.js).

### 7.5. Thiết kế API /predict

- URL/path: `/predict`
- HTTP method: `POST`
- Input fields: `studytime`, `failures`, `absences`, `schoolsup`, `famsup`, `internet`
- Output fields: `predicted_score`, `predicted_score_10`, `model_name`, `message`
- Validation:
  - `studytime`: 1-4
  - `failures`: 0-4
  - `absences`: 0-93
  - `schoolsup`, `famsup`, `internet`: 0 hoặc 1

Example request:

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

Example response:

```json
{
  "predicted_score": 12.8,
  "predicted_score_10": 6.4,
  "model_name": "LinearRegression-web_minimal",
  "message": "Prediction completed successfully."
}
```

Minh chứng: [ml-service/app/schemas/request.py](ml-service/app/schemas/request.py), [ml-service/app/schemas/response.py](ml-service/app/schemas/response.py), [docs/api/predict-api.md](docs/api/predict-api.md).

### 7.6. Thiết kế cơ sở dữ liệu lưu lịch sử dự đoán

Bảng `PredictionHistory` gồm các cột: `Id`, `StudentName`, `ClassName`, `StudyTime`, `Failures`, `Absences`, `SchoolSup`, `FamSup`, `Internet`, `Note`, `PredictedScore`, `PredictedScore10`, `ModelName`, `CreatedAt`. Minh chứng: [database/schema/001_init.sql](database/schema/001_init.sql). Migration bổ sung `PredictedScore10` nằm ở [database/migrations/002_add_predicted_score_10.sql](database/migrations/002_add_predicted_score_10.sql).

### 7.7. Thiết kế giao diện người dùng

Giao diện gồm phần hero, form nhập thông tin học sinh, khu vực kết quả dự đoán, tóm tắt dữ liệu gần nhất và bảng lịch sử dự đoán. Các trường nhập gồm họ tên, lớp, `studytime`, `absences`, `failures`, `schoolsup`, `famsup`, `internet`, ghi chú. Minh chứng: [webapp/PredictTheScore.Web/Views/Home/Index.cshtml](webapp/PredictTheScore.Web/Views/Home/Index.cshtml). Nên vẽ các sơ đồ trong báo cáo: kiến trúc tổng thể, luồng dự đoán, bảng database.

## 8. Xây dựng ứng dụng

### 8.1. Cài đặt môi trường

Backend cần Python và các thư viện trong [ml-service/requirements.txt](ml-service/requirements.txt). Frontend cần .NET 8, minh chứng: [webapp/PredictTheScore.Web/PredictTheScore.Web.csproj](webapp/PredictTheScore.Web/PredictTheScore.Web.csproj). MySQL có thể chạy qua Docker Compose, minh chứng: [docker-compose.yml](docker-compose.yml).

### 8.2. Xây dựng chức năng nhập dữ liệu học sinh

Form nhập dữ liệu nằm trong [webapp/PredictTheScore.Web/Views/Home/Index.cshtml](webapp/PredictTheScore.Web/Views/Home/Index.cshtml). Model validation phía MVC nằm trong [webapp/PredictTheScore.Web/Models/PredictionInputModel.cs](webapp/PredictTheScore.Web/Models/PredictionInputModel.cs). JavaScript kiểm tra form và tạo payload ở [webapp/PredictTheScore.Web/wwwroot/js/script.js](webapp/PredictTheScore.Web/wwwroot/js/script.js).

### 8.3. Xây dựng chức năng gọi API dự đoán

Browser gửi dữ liệu đến `/Predict/Submit`. Controller chuyển dữ liệu thành `PredictionRequestDto`, sau đó `MlApiClient` gọi FastAPI `/predict`. Minh chứng: [webapp/PredictTheScore.Web/Controllers/PredictController.cs](webapp/PredictTheScore.Web/Controllers/PredictController.cs), [webapp/PredictTheScore.Web/Services/MlApiClient.cs](webapp/PredictTheScore.Web/Services/MlApiClient.cs).

### 8.4. Xây dựng chức năng hiển thị điểm dự đoán

Frontend đọc `predicted_score` và `predicted_score_10`, hiển thị điểm thang 20 và thang 10. Minh chứng: [webapp/PredictTheScore.Web/wwwroot/js/script.js](webapp/PredictTheScore.Web/wwwroot/js/script.js), [webapp/PredictTheScore.Web/Views/Home/Index.cshtml](webapp/PredictTheScore.Web/Views/Home/Index.cshtml).

### 8.5. Xây dựng chức năng lưu lịch sử dự đoán

Sau khi nhận kết quả từ ML API, `PredictController` gọi `_historyService.SaveAsync`. Service dùng MySqlConnector và raw SQL để insert vào `PredictionHistory`. Minh chứng: [webapp/PredictTheScore.Web/Controllers/PredictController.cs](webapp/PredictTheScore.Web/Controllers/PredictController.cs), [webapp/PredictTheScore.Web/Services/PredictionHistoryService.cs](webapp/PredictTheScore.Web/Services/PredictionHistoryService.cs).

### 8.6. Xây dựng chức năng xem lịch sử dự đoán

Endpoint MVC `GET /Predict/History` đọc danh sách lịch sử mới nhất và JavaScript gọi endpoint này khi tải trang hoặc sau khi dự đoán. Minh chứng: [webapp/PredictTheScore.Web/Controllers/PredictController.cs](webapp/PredictTheScore.Web/Controllers/PredictController.cs), [webapp/PredictTheScore.Web/wwwroot/js/script.js](webapp/PredictTheScore.Web/wwwroot/js/script.js).

### 8.7. Docker hóa hệ thống

Docker Compose định nghĩa ba service: `db` dùng `mysql:8.4`, `ml-service`, `webapp`. Ports: MySQL `3306`, FastAPI `8000`, webapp `8080`. Minh chứng: [docker-compose.yml](docker-compose.yml). File này có chứa credential môi trường cho MySQL; khi đưa vào báo cáo, không ghi password thật, chỉ ghi `[SECRET DETECTED - DO NOT INCLUDE]`.

### 8.8. Hướng dẫn chạy chương trình

Các bước dựa trên file hiện có:

```bash
python scripts/download_data.py
python scripts/build_dataset.py
python scripts/train_model.py --scenario web_minimal
python scripts/evaluate_model.py
python scripts/compare_models.py
python scripts/export_sample_input.py
cd ml-service
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
dotnet run --project webapp/PredictTheScore.Web/PredictTheScore.Web.csproj
docker compose up --build
```

Lưu ý: README hướng dẫn `cd PredictTheScore.Web`, nhưng trong repository đường dẫn thực tế là `webapp/PredictTheScore.Web`. Minh chứng: [README.md](README.md), [webapp/PredictTheScore.Web/PredictTheScore.Web.csproj](webapp/PredictTheScore.Web/PredictTheScore.Web.csproj).

## 9. Thực nghiệm và kết quả

### 9.1. Kết quả tiền xử lý dữ liệu

Kết quả audit: 1044 dòng thô, 21 dòng trùng, 1023 dòng sau làm sạch, không có dòng thiếu hoặc sai miền giá trị theo audit hiện tại. Minh chứng: [reports/processing_audit.json](reports/processing_audit.json).

### 9.2. Kết quả phân tích tương quan

Ma trận Pearson được lưu tại [reports/tables/pearson_correlation.csv](reports/tables/pearson_correlation.csv), heatmap tại [reports/figures/pearson_heatmap.png](reports/figures/pearson_heatmap.png). Hình `scatter_g2_g3.png` nên dùng để minh họa quan hệ giữa điểm quá trình `G2` và điểm cuối kỳ `G3`.

### 9.3. Kết quả huấn luyện mô hình

Mô hình chính `web_minimal` dùng 6 biến, target `G3`, train/test split 80/20, random state 42. Hệ số và intercept được lưu trong [reports/tables/metrics_web_minimal.json](reports/tables/metrics_web_minimal.json), model artifact ở `ml-service/artifacts/model.joblib`.

### 9.4. Kết quả đánh giá mô hình

Kết quả test của `web_minimal`: MAE 2.3173, MSE 10.6394, RMSE 3.2618, R² 0.0902. Minh chứng: [reports/tables/evaluation_web_minimal.json](reports/tables/evaluation_web_minimal.json). Hình actual-vs-predicted nằm ở [reports/figures/actual_vs_predicted_web_minimal.png](reports/figures/actual_vs_predicted_web_minimal.png).

### 9.5. Kết quả thử nghiệm API

Test backend có 7 test và đã chạy pass. Các test kiểm tra `/health`, `/model-info`, input hợp lệ, `studytime` không hợp lệ, thiếu field, score trong khoảng 0-20 và score thang 10 trong khoảng 0-10. Minh chứng: [ml-service/tests/test_predict_api.py](ml-service/tests/test_predict_api.py). Lệnh đã chạy: `py -m pytest ml-service\tests`, kết quả tóm tắt: `7 passed, 1 warning`.

### 9.6. Kết quả demo giao diện web

Repository có giao diện form và script xử lý demo, nhưng không có ảnh chụp màn hình demo thật. Vì vậy mục ảnh giao diện cần bổ sung bằng cách chạy webapp và chụp các màn hình: form nhập liệu, kết quả dự đoán, bảng lịch sử, Swagger FastAPI. Tình trạng: **Not found in the current project** đối với screenshot.

### 9.7. Nhận xét ưu điểm và hạn chế

Ưu điểm: project có đủ pipeline dữ liệu, model, API, frontend, database, Docker và test backend. Có report artifacts phục vụ báo cáo. Hạn chế: mô hình `web_minimal` có R² thấp; thông tin phân công thành viên chưa có bằng chứng; chưa thấy test tự động frontend; chưa thấy ảnh demo trong repo; các file README hiện có một số đoạn bị lỗi mã hóa tiếng Việt khi đọc bằng terminal, cần kiểm tra lại encoding trước khi đưa vào báo cáo.

## 10. Kết luận và định hướng phát triển

### 10.1. Kết quả đạt được

Project đã xây dựng được một hệ thống dự đoán điểm số học sinh hoàn chỉnh ở mức đồ án: xử lý dữ liệu UCI Student Performance, huấn luyện mô hình hồi quy tuyến tính, tạo API dự đoán bằng FastAPI, giao diện nhập liệu bằng ASP.NET Core MVC, lưu lịch sử vào MySQL, Docker hóa hệ thống và có test backend. Minh chứng nằm ở các file [scripts/build_dataset.py](scripts/build_dataset.py), [scripts/train_model.py](scripts/train_model.py), [ml-service/app/main.py](ml-service/app/main.py), [webapp/PredictTheScore.Web/Controllers/PredictController.cs](webapp/PredictTheScore.Web/Controllers/PredictController.cs), [database/schema/001_init.sql](database/schema/001_init.sql).

### 10.2. Hạn chế của đồ án

Hạn chế lớn nhất là mô hình dùng cho web `web_minimal` chỉ có 6 biến, dẫn đến R² test thấp khoảng 0.0902. Kịch bản `reference` có kết quả tốt hơn nhưng cần thêm `G1`, `G2`, hiện không có trên form web. Ngoài ra repository chưa có bằng chứng rõ về phân công thành viên, screenshot demo, test frontend và quy trình triển khai production.

### 10.3. Hướng phát triển

Có thể mở rộng bằng cách thêm trường `G1`, `G2` hoặc các biến quan trọng hơn vào form nếu mục tiêu là tăng độ chính xác; thử thêm mô hình khác như Decision Tree, Random Forest hoặc Gradient Boosting; thêm dashboard thống kê lịch sử; thêm xác thực người dùng; bổ sung test frontend; thêm migration database hoàn chỉnh; và chuẩn hóa encoding tài liệu tiếng Việt.

## 11. Tài liệu tham khảo

Danh sách tham khảo đề xuất dựa trên công nghệ và dữ liệu thực tế trong project:

1. UCI Machine Learning Repository - Student Performance Dataset. Minh chứng project: [scripts/download_data.py](scripts/download_data.py), [data/raw/student.txt](data/raw/student.txt). Citation chính xác cần kiểm tra từ nguồn UCI: **Need confirmation**.
2. FastAPI official documentation. Công nghệ dùng trong [ml-service/app/main.py](ml-service/app/main.py), [ml-service/requirements.txt](ml-service/requirements.txt).
3. scikit-learn documentation: `LinearRegression`, `train_test_split`, regression metrics. Minh chứng: [scripts/train_model.py](scripts/train_model.py).
4. pandas documentation. Minh chứng: [scripts/build_dataset.py](scripts/build_dataset.py).
5. matplotlib documentation. Minh chứng: [scripts/build_dataset.py](scripts/build_dataset.py), [scripts/evaluate_model.py](scripts/evaluate_model.py).
6. ASP.NET Core MVC documentation. Minh chứng: [webapp/PredictTheScore.Web/PredictTheScore.Web.csproj](webapp/PredictTheScore.Web/PredictTheScore.Web.csproj), [webapp/PredictTheScore.Web/Program.cs](webapp/PredictTheScore.Web/Program.cs).
7. MySQL documentation. Minh chứng: [database/schema/001_init.sql](database/schema/001_init.sql), [docker-compose.yml](docker-compose.yml).
8. Docker Compose documentation. Minh chứng: [docker-compose.yml](docker-compose.yml).

## 12. Phụ lục

- Link GitHub: `https://github.com/Mei-iwi/Predict_The_Score.git`. Minh chứng: lệnh `git remote -v`.
- Hình ảnh giao diện cần chụp:
  - Trang form nhập liệu.
  - Kết quả dự đoán thang 20 và thang 10.
  - Bảng lịch sử dự đoán.
  - Swagger `/docs`.
  - Docker containers nếu chạy bằng Docker.
- Mã nguồn chính cần trích:
  - [scripts/build_dataset.py](scripts/build_dataset.py)
  - [scripts/train_model.py](scripts/train_model.py)
  - [scripts/compare_models.py](scripts/compare_models.py)
  - [ml-service/app/main.py](ml-service/app/main.py)
  - [ml-service/app/schemas/request.py](ml-service/app/schemas/request.py)
  - [ml-service/app/services/predictor.py](ml-service/app/services/predictor.py)
  - [webapp/PredictTheScore.Web/Controllers/PredictController.cs](webapp/PredictTheScore.Web/Controllers/PredictController.cs)
  - [webapp/PredictTheScore.Web/Services/PredictionHistoryService.cs](webapp/PredictTheScore.Web/Services/PredictionHistoryService.cs)
  - [webapp/PredictTheScore.Web/wwwroot/js/script.js](webapp/PredictTheScore.Web/wwwroot/js/script.js)
- File dữ liệu mẫu:
  - [data/samples/sample_input.csv](data/samples/sample_input.csv)
  - [data/samples/sample_input.json](data/samples/sample_input.json)
- Bảng commit GitHub của từng thành viên: **Need confirmation** vì repository chưa đủ bằng chứng gắn commit với từng thành viên.
- Danh sách lệnh đã chạy để kiểm tra project:
  - `git status --short`: xem thay đổi hiện tại.
  - `rg --files`: liệt kê file trong project.
  - `git log --oneline --all --decorate -n 30`: xem lịch sử commit.
  - `git remote -v`: xác định remote GitHub.
  - `py scripts\build_dataset.py`: pass, tạo audit/dataset/figures.
  - `py scripts\train_model.py --scenario web_minimal`: pass, lưu model và metrics.
  - `py scripts\evaluate_model.py`: pass, lưu evaluation và hình actual-vs-predicted.
  - `py scripts\compare_models.py`: pass, lưu model comparison và coefficients.
  - `py scripts\export_sample_input.py`: pass, tạo sample input.
  - `py -m pytest ml-service\tests`: pass 7 tests, có 1 warning từ dependency.
  - `dotnet build webapp\PredictTheScore.Web\PredictTheScore.Web.csproj`: pass, 0 warning, 0 error.
- Danh sách file minh chứng quan trọng:
  - [reports/processing_audit.json](reports/processing_audit.json)
  - [reports/tables/model_comparison.csv](reports/tables/model_comparison.csv)
  - [reports/tables/metrics_web_minimal.json](reports/tables/metrics_web_minimal.json)
  - [reports/tables/evaluation_web_minimal.json](reports/tables/evaluation_web_minimal.json)
  - [reports/figures/pearson_heatmap.png](reports/figures/pearson_heatmap.png)
  - [reports/figures/actual_vs_predicted_web_minimal.png](reports/figures/actual_vs_predicted_web_minimal.png)

## 13. Checklist nội dung còn thiếu để hoàn thiện báo cáo

| STT | Nội dung còn thiếu/cần xác nhận | Mức độ quan trọng | Gợi ý cách bổ sung | File/khu vực liên quan |
| --- | --- | --- | --- | --- |
| 1 | Danh sách thành viên nhóm | Cao | Bổ sung tên, MSSV, vai trò vào docs hoặc báo cáo | [docs/progress/week-01.md](docs/progress/week-01.md) |
| 2 | Phân công chi tiết theo người | Cao | Nhóm xác nhận ai làm dữ liệu, model, backend, frontend, database, docs | [docs/progress/week-*.md](docs/progress/week-01.md) |
| 3 | Ảnh chụp giao diện demo | Cao | Chạy webapp, chụp form, kết quả, history | [webapp/PredictTheScore.Web/Views/Home/Index.cshtml](webapp/PredictTheScore.Web/Views/Home/Index.cshtml) |
| 4 | Ảnh Swagger API | Trung bình | Chạy FastAPI và chụp `/docs` | [ml-service/app/main.py](ml-service/app/main.py) |
| 5 | Citation dataset chuẩn | Cao | Lấy thông tin trích dẫn từ UCI hoặc `student.txt` | [data/raw/student.txt](data/raw/student.txt) |
| 6 | Test frontend tự động | Thấp/Trung bình | Có thể bổ sung manual test hoặc Playwright/Selenium nếu cần | [tests/manual/test_cases.md](tests/manual/test_cases.md) |
| 7 | Nhận xét của nhóm về hạn chế mô hình | Trung bình | Giải thích vì sao `web_minimal` R² thấp và hướng cải thiện | [reports/tables/model_comparison.csv](reports/tables/model_comparison.csv) |
| 8 | Password trong Docker/appsettings | Cao | Không đưa password thật vào báo cáo, dùng `[SECRET DETECTED - DO NOT INCLUDE]` | [docker-compose.yml](docker-compose.yml), [webapp/PredictTheScore.Web/appsettings.json](webapp/PredictTheScore.Web/appsettings.json) |

## 14. Evidence map

| Nội dung báo cáo | File/thư mục minh chứng | Ghi chú |
| --- | --- | --- |
| Tổng quan project | [README.md](README.md), [docs/architecture/architecture-overview.md](docs/architecture/architecture-overview.md) | README có một số đoạn tiếng Việt bị lỗi encoding khi đọc terminal |
| GitHub/commit history | `git remote -v`, `git log --oneline --all --decorate -n 30` | Có remote và commit history, chưa đủ phân công cá nhân |
| Dữ liệu nguồn | [data/raw/student-mat.csv](data/raw/student-mat.csv), [data/raw/student-por.csv](data/raw/student-por.csv), [data/raw/student.txt](data/raw/student.txt) | UCI Student Performance |
| Xử lý dữ liệu | [scripts/build_dataset.py](scripts/build_dataset.py), [reports/processing_audit.json](reports/processing_audit.json) | Chọn cột, mã hóa, drop duplicates, audit |
| Dữ liệu sạch | [data/processed/student_performance_clean.csv](data/processed/student_performance_clean.csv) | 1023 dòng sau cleaning |
| Feature config | [data/processed/feature_config.json](data/processed/feature_config.json) | `reference`, `early_warning`, `web_minimal` |
| Tương quan Pearson | [reports/tables/pearson_correlation.csv](reports/tables/pearson_correlation.csv), [reports/figures/pearson_heatmap.png](reports/figures/pearson_heatmap.png) | Có bảng và hình |
| Huấn luyện model | [scripts/train_model.py](scripts/train_model.py), [reports/tables/metrics_web_minimal.json](reports/tables/metrics_web_minimal.json) | LinearRegression |
| So sánh model | [scripts/compare_models.py](scripts/compare_models.py), [reports/tables/model_comparison.csv](reports/tables/model_comparison.csv) | `reference` tốt nhất theo RMSE |
| Đánh giá model | [scripts/evaluate_model.py](scripts/evaluate_model.py), [reports/tables/evaluation_web_minimal.json](reports/tables/evaluation_web_minimal.json), [reports/figures/actual_vs_predicted_web_minimal.png](reports/figures/actual_vs_predicted_web_minimal.png) | Evaluation cho model web |
| Backend API | [ml-service/app/main.py](ml-service/app/main.py), [ml-service/app/schemas/request.py](ml-service/app/schemas/request.py), [ml-service/app/schemas/response.py](ml-service/app/schemas/response.py) | `/predict`, `/health`, `/model-info` |
| Model loader/predictor | [ml-service/app/services/model_loader.py](ml-service/app/services/model_loader.py), [ml-service/app/services/predictor.py](ml-service/app/services/predictor.py) | Nạp model và clip score 0-20 |
| Frontend MVC | [webapp/PredictTheScore.Web/Program.cs](webapp/PredictTheScore.Web/Program.cs), [webapp/PredictTheScore.Web/Views/Home/Index.cshtml](webapp/PredictTheScore.Web/Views/Home/Index.cshtml) | Form và UI |
| Frontend API integration | [webapp/PredictTheScore.Web/Controllers/PredictController.cs](webapp/PredictTheScore.Web/Controllers/PredictController.cs), [webapp/PredictTheScore.Web/Services/MlApiClient.cs](webapp/PredictTheScore.Web/Services/MlApiClient.cs), [webapp/PredictTheScore.Web/wwwroot/js/script.js](webapp/PredictTheScore.Web/wwwroot/js/script.js) | Gửi request và hiển thị response |
| Database history | [database/schema/001_init.sql](database/schema/001_init.sql), [database/migrations/002_add_predicted_score_10.sql](database/migrations/002_add_predicted_score_10.sql), [webapp/PredictTheScore.Web/Services/PredictionHistoryService.cs](webapp/PredictTheScore.Web/Services/PredictionHistoryService.cs) | Raw SQL, MySQL |
| Docker | [docker-compose.yml](docker-compose.yml), [ml-service/Dockerfile](ml-service/Dockerfile), [webapp/PredictTheScore.Web/Dockerfile](webapp/PredictTheScore.Web/Dockerfile) | 3 service: db, ml-service, webapp |
| Test backend | [ml-service/tests/test_predict_api.py](ml-service/tests/test_predict_api.py) | 7 test pass |
| Manual test | [tests/manual/test_cases.md](tests/manual/test_cases.md) | Checklist thủ công |
