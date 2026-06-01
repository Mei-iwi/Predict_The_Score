# PROJECT_IMPROVEMENT_PLAN.md

Tài liệu này đánh giá hiện trạng repository và đề xuất kế hoạch cải thiện cho đồ án môn **Khai phá dữ liệu / Data Mining** với đề tài **"Xây dựng ứng dụng để dự đoán điểm số của học sinh"**. Nội dung chỉ dựa trên bằng chứng hiện có trong project, không tự khẳng định các phần chưa có minh chứng.

## 1. Tổng quan dự án hiện tại

| Nội dung kiểm tra | Kết quả hiện tại | Minh chứng file/thư mục | Nhận xét |
| --- | --- | --- | --- |
| Tên project | Predict The Score / Predict_The_Score | `README.md`, `git remote -v` | Remote GitHub: `https://github.com/Mei-iwi/Predict_The_Score.git` |
| Mục đích chính | Dự đoán điểm cuối kỳ `G3` của học sinh | `scripts/train_model.py`, `data/processed/feature_config.json`, `ml-service/app/main.py` | Phù hợp đề tài hồi quy dự đoán điểm số |
| Kiến trúc hiện tại | Frontend ASP.NET Core MVC, backend FastAPI, MySQL, scripts ML/data | `docs/architecture/architecture-overview.md`, `docker-compose.yml` | Kiến trúc tách frontend/backend rõ ràng |
| Công nghệ chính | Python, pandas, scikit-learn, matplotlib, FastAPI, Pydantic, joblib, ASP.NET Core MVC, MySQL, Docker | `ml-service/requirements.txt`, `webapp/PredictTheScore.Web/PredictTheScore.Web.csproj`, `docker-compose.yml` | Công nghệ đủ cho đồ án ứng dụng Data Mining |
| Dữ liệu | UCI Student Performance, gồm `student-mat.csv`, `student-por.csv` | `data/raw/student-mat.csv`, `data/raw/student-por.csv`, `scripts/download_data.py` | Có dữ liệu thô trong project |
| Xử lý dữ liệu | Chọn cột, bỏ trùng, mã hóa yes/no, kiểm tra miền giá trị, tạo audit | `scripts/build_dataset.py`, `reports/processing_audit.json` | Đáp ứng yêu cầu preprocessing |
| Phân tích dữ liệu | Pearson correlation, heatmap, histogram absences, scatter G2-G3 | `reports/tables/pearson_correlation.csv`, `reports/figures/pearson_heatmap.png`, `reports/figures/hist_absences.png`, `reports/figures/scatter_g2_g3.png` | Cần bổ sung mô tả/nhận xét chi tiết hơn cho báo cáo |
| Mô hình | `LinearRegression` | `scripts/train_model.py`, `scripts/compare_models.py` | Phù hợp bài toán hồi quy |
| Đánh giá mô hình | MAE, MSE, RMSE, R²; có train/test metrics và model comparison | `reports/tables/metrics_web_minimal.json`, `reports/tables/model_comparison.csv`, `reports/tables/evaluation_web_minimal.json` | Có bằng chứng tốt, cần giải thích hạn chế R² thấp của `web_minimal` |
| Backend | FastAPI có `/`, `/health`, `/model-info`, `/predict` | `ml-service/app/main.py`, `ml-service/app/schemas/request.py`, `ml-service/app/schemas/response.py` | API rõ, có validation |
| Frontend | Form nhập dữ liệu, gọi MVC endpoint, hiển thị kết quả, tải history | `webapp/PredictTheScore.Web/Views/Home/Index.cshtml`, `webapp/PredictTheScore.Web/wwwroot/js/script.js`, `webapp/PredictTheScore.Web/Controllers/PredictController.cs` | Có ứng dụng web hoạt động |
| Lưu lịch sử | MySQL table `PredictionHistory`, raw SQL qua `MySqlConnector` | `database/schema/001_init.sql`, `webapp/PredictTheScore.Web/Services/PredictionHistoryService.cs` | Đáp ứng yêu cầu lưu lịch sử |
| Docker | Có `db`, `ml-service`, `webapp` | `docker-compose.yml`, `ml-service/Dockerfile`, `webapp/PredictTheScore.Web/Dockerfile` | Có thể demo bằng Docker; không đưa mật khẩu thật vào báo cáo |
| Test | Có 7 test backend API | `ml-service/tests/test_predict_api.py` | Chưa thấy test tự động frontend |
| Báo cáo nguồn | Đã có tài liệu nguồn báo cáo | `REPORT_SOURCE_MATERIAL.md` | Có thể dùng để viết Word report |
| Slide PowerPoint | Not found in current project | Không thấy file `.pptx` hoặc thư mục slide | Cần tạo trước khi nộp |
| Ảnh demo giao diện | Not found in current project | Không thấy thư mục screenshots | Cần chụp bổ sung |
| Phân công thành viên | Need confirmation | `docs/progress/week-01.md`, `week-02.md`, `week-03.md` đang để `TBD` | Cần nhóm bổ sung |

## 2. Đối chiếu dự án với yêu cầu đề tài

| Yêu cầu đề tài | Tình trạng trong project | Mức độ đạt | Minh chứng | Cần cải thiện |
| --- | --- | --- | --- | --- |
| Có bộ dữ liệu hoặc quy trình xây dựng dữ liệu | Có dataset UCI và script download | Đạt | `data/raw/student-mat.csv`, `data/raw/student-por.csv`, `scripts/download_data.py` | Bổ sung citation dataset rõ trong báo cáo |
| Có làm sạch / tiền xử lý dữ liệu | Có chọn cột, bỏ trùng, mã hóa, kiểm tra miền giá trị | Đạt | `scripts/build_dataset.py`, `reports/processing_audit.json` | Thêm mô tả bằng tiếng Việt trong docs |
| Có phân tích dữ liệu | Có Pearson, heatmap, histogram, scatter | Khá | `reports/tables/pearson_correlation.csv`, `reports/figures/*.png` | Viết nhận xét dữ liệu và diễn giải tương quan |
| Có áp dụng mô hình hồi quy | Có `LinearRegression` | Đạt | `scripts/train_model.py` | Có thể giải thích vì sao chọn Linear Regression |
| Có đánh giá mô hình | Có MAE, MSE, RMSE, R² | Đạt | `reports/tables/metrics_web_minimal.json`, `reports/tables/model_comparison.csv` | Thêm bảng tổng hợp đẹp hơn cho báo cáo nếu cần |
| Có ứng dụng web học tập | Có ASP.NET Core MVC webapp | Đạt | `webapp/PredictTheScore.Web/` | Cần ảnh demo giao diện |
| Có backend phục vụ dự đoán | Có FastAPI | Đạt | `ml-service/app/main.py` | Cần ảnh Swagger `/docs` |
| Có frontend nhập dữ liệu và hiển thị kết quả | Có form, JS, result panel | Đạt | `Views/Home/Index.cshtml`, `wwwroot/js/script.js` | Có thể chỉnh input `max` HTML cho `absences/failures` khớp validation nếu muốn |
| Có lưu lịch sử dự đoán | Có MySQL và service lưu history | Đạt | `PredictionHistoryService.cs`, `database/schema/001_init.sql` | Cần demo database hoặc screenshot history |
| Có hướng dẫn chạy chương trình | Có README và docs | Khá | `README.md`, `docs/architecture/architecture-overview.md` | README bị lỗi encoding khi đọc terminal; nên chuẩn hóa lại tiếng Việt |
| Có báo cáo, slide, hình ảnh minh chứng | Có `REPORT_SOURCE_MATERIAL.md`, reports figures/tables; chưa thấy slide/screenshot | Một phần | `REPORT_SOURCE_MATERIAL.md`, `reports/figures/` | Tạo Word report, PowerPoint, screenshots |

## 3. Đối chiếu dự án với rubric chấm điểm

| Tiêu chí rubric | Trọng số | Tình trạng hiện tại | Điểm mạnh | Điểm yếu | Việc cần làm để đạt điểm cao |
| --- | ---: | --- | --- | --- | --- |
| Thu thập/xây dựng và phân tích dữ liệu | 15% | Có dataset thô, data clean, Pearson outputs | Có dữ liệu thật, có audit và figures | Nhận xét phân tích còn nằm rải rác, chưa có tài liệu phân tích riêng | Tạo `docs/data-analysis.md`, bổ sung nhận xét từng hình/bảng; dùng `reports/tables/pearson_correlation.csv`, `reports/figures/*.png` |
| Làm sạch dữ liệu / tiền xử lý dữ liệu | 15% | Có script preprocessing và audit rõ | Có duplicate count, row counts, encoding rule | Code có ít comment tiếng Việt giải thích từng bước | Bổ sung docstring/comment trong `scripts/build_dataset.py`, tạo bảng preprocessing trong report |
| Mô hình / kỹ thuật xử lý bài toán | 20% | Có LinearRegression, train/test split, metrics, comparison | Có 3 scenario, có coefficients | `web_minimal` R² thấp; chưa thử mô hình khác | Giải thích trade-off; nếu còn thời gian, thêm thử nghiệm đơn giản `DecisionTreeRegressor` trong `scripts/compare_models.py` nhưng không đổi model chính nếu không cần |
| Xây dựng ứng dụng | 30% | Có backend, frontend, DB, Docker | Chức năng end-to-end tương đối đầy đủ | Chưa có screenshot demo; chưa có test frontend | Chụp giao diện, Swagger, history; tạo `docs/demo-guide.md`; kiểm tra Docker demo |
| Trình bày báo cáo | 10% | Có `REPORT_SOURCE_MATERIAL.md` và docs | Có nhiều bằng chứng sẵn | Chưa có Word report/PowerPoint trong repo | Tạo Word report và slide dựa trên `REPORT_SOURCE_MATERIAL.md`; tạo `docs/report-evidence.md` |
| Phân công và phối hợp nhóm | 10% | Chưa có bằng chứng đủ | Có git log và progress files | Thành viên, vai trò, minh chứng đóng góp chưa rõ | Cập nhật `docs/teamwork.md` hoặc `docs/progress/week-*.md` với thành viên thật, commit/link minh chứng |

## 4. Đối chiếu dự án với khung báo cáo Word

| Mục báo cáo | Nội dung cần có | Dữ liệu/source hiện có | Nội dung còn thiếu | File cần bổ sung/chỉnh sửa |
| --- | --- | --- | --- | --- |
| 1. Lịch làm việc nhóm theo tuần | Kế hoạch, tiến độ, kết quả từng tuần | `docs/progress/week-01.md`, `week-02.md`, `week-03.md`, git log | Người phụ trách và evidence commit cụ thể | Cập nhật `docs/progress/week-*.md`, tạo `docs/teamwork.md` |
| 2. Phân công công việc thành viên | Danh sách thành viên, bảng phân công, minh chứng | Git log, branch `mainhatcuong` | Danh sách thành viên chính thức | `docs/teamwork.md` |
| 3. Giới thiệu đề tài | Lý do, mục tiêu, phạm vi, đối tượng | `README.md`, `REPORT_SOURCE_MATERIAL.md` | Nội dung final report cần biên tập lại | Word report |
| 4. Cơ sở lý thuyết | Data mining, regression, Pearson, metrics | `REPORT_SOURCE_MATERIAL.md`, scripts ML | Tài liệu tham khảo chuẩn | Word report, `docs/references.md` nếu cần |
| 5. Phân tích dữ liệu | Nguồn, thuộc tính, cleaning, correlation | `scripts/build_dataset.py`, `reports/processing_audit.json`, `reports/tables/pearson_correlation.csv` | Nhận xét chi tiết từng output | `docs/data-analysis.md` |
| 6. Thiết kế mô hình dự đoán | Feature scenarios, model, train/test, metrics | `feature_config.json`, `train_model.py`, `model_comparison.csv` | Giải thích hạn chế và lý do chọn `web_minimal` | `docs/model-training.md` |
| 7. Thiết kế hệ thống | Kiến trúc, API, DB, UI | `docs/architecture/architecture-overview.md`, `docs/api/predict-api.md`, `docs/database/schema-note.md` | Sơ đồ kiến trúc dạng hình | `reports/figures/architecture_diagram.png`, `reports/figures/prediction_flow.png` |
| 8. Xây dựng ứng dụng | Cài đặt, chức năng, Docker, run guide | `README.md`, `docker-compose.yml`, source backend/frontend | README cần chuẩn hóa encoding và đường dẫn | `README.md`, `docs/demo-guide.md` |
| 9. Thực nghiệm và kết quả | Preprocessing, correlation, train/eval, API test, demo UI | `reports/`, `ml-service/tests/test_predict_api.py` | Screenshot demo và Docker running | `docs/screenshots/README.md`, ảnh chụp |
| 10. Kết luận và hướng phát triển | Kết quả, hạn chế, hướng phát triển | `REPORT_SOURCE_MATERIAL.md`, metrics | Nội dung final report | Word report |
| 11. Tài liệu tham khảo | Dataset, framework, thư viện | `student.txt`, `requirements.txt`, csproj | Citation dataset chuẩn | `docs/references.md` hoặc phần references trong report |
| 12. Phụ lục | GitHub, screenshots, code chính, sample data, commit table | `git remote -v`, `data/samples/`, `git log` | Commit theo từng thành viên, screenshot | `docs/teamwork.md`, `docs/screenshots/README.md` |

## 5. Danh sách cải thiện source code cần thực hiện

| STT | Hạng mục cải thiện | Lý do cần cải thiện | File cần sửa/tạo | Mức ưu tiên | Cách kiểm tra sau khi sửa |
| --- | --- | --- | --- | --- | --- |
| 1 | Chuẩn hóa README tiếng Việt và đường dẫn chạy frontend | README hiện có dấu hiệu lỗi encoding và có hướng dẫn `cd PredictTheScore.Web` chưa khớp cấu trúc repo | `README.md` | P0 | Đọc lại README, chạy theo hướng dẫn |
| 2 | Bổ sung comment/docstring tiếng Việt cho data pipeline | Giúp dễ giải thích trong vấn đáp | `scripts/build_dataset.py` | P0 | Chạy `py scripts\build_dataset.py` |
| 3 | Bổ sung comment cho training/evaluation | Giải thích feature selection, split, metrics, model saving | `scripts/train_model.py`, `scripts/evaluate_model.py`, `scripts/compare_models.py` | P0 | Chạy train/evaluate/compare |
| 4 | Tạo tài liệu phân tích dữ liệu riêng | Báo cáo cần phần data analysis rõ | `docs/data-analysis.md` | P0 | Đối chiếu với `reports/processing_audit.json` |
| 5 | Tạo tài liệu model training riêng | Giải thích scenario và kết quả metrics | `docs/model-training.md` | P0 | Đối chiếu với `model_comparison.csv` |
| 6 | Tạo demo guide và screenshot checklist | Final submission cần hình minh chứng | `docs/demo-guide.md`, `docs/screenshots/README.md` | P0 | Chạy app và tick đủ screenshot |
| 7 | Bổ sung teamwork evidence | Rubric có 10% teamwork | `docs/teamwork.md`, `docs/progress/week-*.md` | P0 | Có tên thành viên, vai trò, commit/evidence |
| 8 | Kiểm tra HTML validation max/min | View đang để `absences max=100`, `failures max=10` trong HTML, trong backend là 93 và 4 | `webapp/PredictTheScore.Web/Views/Home/Index.cshtml` | P1 | Submit giá trị biên, kiểm tra frontend/backend |
| 9 | Bổ sung comment cho API and schemas | Swagger/API dễ giải thích hơn | `ml-service/app/main.py`, `schemas/request.py`, `schemas/response.py` | P1 | Mở `/docs`, chạy pytest |
| 10 | Bổ sung comment cho MVC controller/service | Giải thích luồng frontend -> backend -> DB | `PredictController.cs`, `MlApiClient.cs`, `PredictionHistoryService.cs` | P1 | `dotnet build` |
| 11 | Tạo `reports/tables/model_metrics.csv` tổng hợp train/test | Dễ đưa vào Word/slide hơn JSON | Có thể tạo từ `metrics_web_minimal.json` | P1 | File CSV có MAE/MSE/RMSE/R² |
| 12 | Tạo sơ đồ kiến trúc và luồng dự đoán | Báo cáo và slide trực quan hơn | `reports/figures/architecture_diagram.png`, `prediction_flow.png` | P1 | File hình tồn tại |
| 13 | Thêm kiểm thử integration nhẹ nếu có thời gian | Tăng độ tin cậy demo | `tests/integration/` hoặc docs manual | P2 | Checklist chạy end-to-end |
| 14 | Cân nhắc thêm mô hình so sánh đơn giản | Rubric model có 20%, so sánh nhiều model có thể thuyết phục hơn | `scripts/compare_models.py` | P2 | `model_comparison.csv` có thêm model mới |
| 15 | Logging rõ hơn cho backend | Dễ debug khi demo | `ml-service/app/utils/logger.py`, `ml-service/app/main.py` | P2 | Log không chứa secret |

## 6. Yêu cầu bổ sung comment giải thích source code

| File | Hàm/class/đoạn code | Comment cần bổ sung | Mục đích giải thích | Mức ưu tiên |
| --- | --- | --- | --- | --- |
| `scripts/build_dataset.py` | Phần hằng số đường dẫn và cột | Vai trò thư mục data/reports, danh sách cột chọn | Giúp hiểu input/output preprocessing | P0 |
| `scripts/build_dataset.py` | `find_raw_sources` | Cách tìm CSV/ZIP nguồn | Giải thích dataset loading | P0 |
| `scripts/build_dataset.py` | `preprocess_student_performance` | Các bước chọn cột, drop duplicates, encode yes/no, check ranges | Giải thích data cleaning | P0 |
| `scripts/build_dataset.py` | Pearson correlation và `save_figures` | Vì sao sinh Pearson, heatmap, histogram, scatter | Giải thích data analysis | P0 |
| `scripts/train_model.py` | `load_processed_data` | Đọc clean dataset và feature config | Giải thích đầu vào training | P0 |
| `scripts/train_model.py` | Train/test split | Ý nghĩa `test_size=0.2`, `random_state=42` | Giải thích quy trình ML | P0 |
| `scripts/train_model.py` | Bundle model | Các metadata được lưu cùng model | Giải thích tích hợp backend | P0 |
| `scripts/evaluate_model.py` | Evaluation flow | Nạp model, lấy test indices, tính metrics | Giải thích đánh giá model | P0 |
| `scripts/compare_models.py` | Scenario loop | So sánh `reference`, `early_warning`, `web_minimal` | Giải thích lựa chọn mô hình | P0 |
| `ml-service/app/main.py` | `/predict` | Input, output, score thang 20/10 | Giải thích API chính | P0 |
| `ml-service/app/schemas/request.py` | `PredictionRequest` | Validation rules | Giúp hiểu 422 validation | P0 |
| `ml-service/app/services/predictor.py` | `predict_score` | Tạo dataframe, predict, clip 0-20 | Giải thích post-processing | P0 |
| `ml-service/app/services/model_loader.py` | `load_model_bundle` | Lazy load model artifact | Giải thích model loading | P1 |
| `webapp/.../PredictController.cs` | `Submit` | Luồng nhận input, gọi ML API, lưu history | Giải thích backend MVC | P0 |
| `webapp/.../MlApiClient.cs` | `PredictAsync` | Cách gọi FastAPI và xử lý lỗi | Giải thích integration | P0 |
| `webapp/.../PredictionHistoryService.cs` | `SaveAsync`, `GetLatestAsync` | SQL insert/select history | Giải thích lưu lịch sử | P0 |
| `webapp/.../wwwroot/js/script.js` | `getPayload`, `postPrediction`, `normalizeResponse`, `loadHistoryFromDatabase` | Cách frontend gửi/nhận dữ liệu | Giải thích UI logic | P1 |
| `docker-compose.yml` | Service `db`, `ml-service`, `webapp` | Vai trò từng container và port | Giải thích Docker | P1 |

### COMMENTING_GUIDE_FOR_CODEX

Khi thực hiện cải thiện comment cho source code:

- Thêm comment tiếng Việt cho các phần source code quan trọng.
- Giữ comment ngắn gọn, rõ ý, phù hợp sinh viên giải thích khi bảo vệ.
- Không comment từng dòng hiển nhiên.
- Thêm comment trước các khối logic phức tạp hoặc có ý nghĩa nghiệp vụ.
- Thêm docstring cho các hàm/class Python quan trọng.
- Với C#, thêm XML comment hoặc comment thường cho class/method quan trọng nếu phù hợp style hiện tại.
- Giải thích rõ input/output của mô hình, validation rule và ý nghĩa score 0-20, 0-10.
- Không thay đổi hành vi chương trình khi chỉ thêm comment.
- Không ghi secret, password, token hoặc credential vào comment.

## 7. Danh sách file nên tạo mới để hỗ trợ báo cáo

| File đề xuất | Mục đích | Nội dung chính | Liên quan mục báo cáo |
| --- | --- | --- | --- |
| `docs/project-overview.md` | Tổng hợp project ngắn gọn | Mục tiêu, kiến trúc, chức năng | Mục 3, 7, 8 |
| `docs/data-analysis.md` | Viết riêng phần dữ liệu | Nguồn dữ liệu, audit, encoding, Pearson, nhận xét hình | Mục 5, 9 |
| `docs/model-training.md` | Viết riêng phần mô hình | Feature scenarios, LinearRegression, metrics, comparison, hạn chế | Mục 6, 9 |
| `docs/system-design.md` | Thiết kế hệ thống | Kiến trúc, API, DB, frontend/backend flow | Mục 7 |
| `docs/api-spec.md` | API spec tiếng Việt | `/predict`, `/health`, `/model-info`, request/response | Mục 7.5 |
| `docs/demo-guide.md` | Hướng dẫn demo | Run backend/frontend/docker, thứ tự chụp ảnh | Mục 8, 9, 12 |
| `docs/teamwork.md` | Minh chứng phân công | Thành viên, nhiệm vụ, commit/file evidence | Mục 1, 2 |
| `docs/report-evidence.md` | Map chứng cứ báo cáo | File nào dùng cho mục nào trong report | Mục 12 |
| `docs/screenshots/README.md` | Checklist ảnh cần chụp | Form, result, history, Swagger, Docker | Mục 9, 12 |
| `reports/tables/model_metrics.csv` | Bảng metrics dễ copy vào Word | Train/test metrics của model chính | Mục 6, 9 |
| `reports/tables/feature_scenarios.csv` | Bảng scenario dễ trình bày | reference, early_warning, web_minimal | Mục 6 |
| `reports/figures/architecture_diagram.png` | Hình kiến trúc | Browser, MVC, FastAPI, model, MySQL | Mục 7 |
| `reports/figures/prediction_flow.png` | Hình luồng dự đoán | Input -> API -> model -> history | Mục 7, 8 |

## 8. Gợi ý hình ảnh, bảng biểu cần đưa vào báo cáo

| STT | Hình ảnh cần chèn | Nguồn tạo/chụp | Mục báo cáo phù hợp | Ghi chú |
| --- | --- | --- | --- | --- |
| 1 | Cấu trúc thư mục project | Tạo từ `rg --files` hoặc cây thư mục | Mục 7, 8 | Có thể vẽ lại gọn |
| 2 | Pearson correlation heatmap | `reports/figures/pearson_heatmap.png` | Mục 5, 9 | Đã có |
| 3 | Histogram absences | `reports/figures/hist_absences.png` | Mục 5, 9 | Đã có |
| 4 | Scatter G2-G3 | `reports/figures/scatter_g2_g3.png` | Mục 5, 9 | Đã có |
| 5 | Actual vs predicted | `reports/figures/actual_vs_predicted_web_minimal.png` | Mục 6, 9 | Đã có |
| 6 | Sơ đồ kiến trúc | Cần tạo `reports/figures/architecture_diagram.png` | Mục 7 | Chưa thấy file |
| 7 | Sơ đồ luồng dự đoán | Cần tạo `reports/figures/prediction_flow.png` | Mục 7, 8 | Chưa thấy file |
| 8 | Frontend input screen | Chụp webapp | Mục 8, 9 | Not found in current project |
| 9 | Prediction result screen | Chụp sau khi dự đoán | Mục 8, 9 | Not found in current project |
| 10 | Prediction history screen | Chụp bảng history | Mục 8, 9 | Not found in current project |
| 11 | Swagger API screen | Chụp `http://127.0.0.1:8000/docs` | Mục 7, 9 | Not found in current project |
| 12 | Docker running screenshot | Chụp Docker Desktop hoặc terminal | Mục 8, 12 | Not found in current project |

| STT | Bảng biểu cần chèn | Nguồn dữ liệu | Mục báo cáo phù hợp | Ghi chú |
| --- | --- | --- | --- | --- |
| 1 | Dataset file summary | `data/raw/`, `reports/processing_audit.json` | Mục 5 | Nêu 1044 dòng thô, 1023 dòng sạch |
| 2 | Missing/duplicate/invalid summary | `reports/processing_audit.json` | Mục 5, 9 | Đã có audit |
| 3 | Selected columns | `scripts/build_dataset.py`, `reports/processing_audit.json` | Mục 5 | Có danh sách cột |
| 4 | Encoding rules | `scripts/build_dataset.py` | Mục 5 | yes/no -> 1/0 |
| 5 | Feature scenarios | `data/processed/feature_config.json` | Mục 6 | Nên tạo CSV riêng |
| 6 | Model comparison metrics | `reports/tables/model_comparison.csv` | Mục 6, 9 | Đã có |
| 7 | Coefficients/intercept | `reports/tables/model_coefficients.csv`, `metrics_web_minimal.json` | Mục 6 | Đã có |
| 8 | API request/response | `docs/api/predict-api.md`, schemas | Mục 7 | Đã có |
| 9 | Backend test cases | `ml-service/tests/test_predict_api.py` | Mục 9 | Đã có |
| 10 | Git commit contribution table | `git log` | Mục 1, 2, 12 | Cần mapping thành viên: Need confirmation |

## 9. Prompt hoàn chỉnh để đưa lại vào ChatGPT Web

```text
Bạn hãy đọc PROJECT_IMPROVEMENT_PLAN.md và REPORT_SOURCE_MATERIAL.md nếu có. Đây là tài liệu phân tích hiện trạng và nguồn bằng chứng của đồ án môn Khai phá dữ liệu với đề tài "Xây dựng ứng dụng để dự đoán điểm số của học sinh".

Nhiệm vụ của bạn:
1. Viết một prompt triển khai hoàn chỉnh cho Codex để hoàn thiện đồ án theo rubric.
2. Ưu tiên cải thiện theo trọng số rubric: ứng dụng 30%, mô hình 20%, dữ liệu/phân tích 15%, preprocessing 15%, báo cáo 10%, teamwork 10%.
3. Yêu cầu Codex bổ sung tài liệu còn thiếu, evidence cho báo cáo, comment giải thích source code, demo guide, screenshot checklist, teamwork docs.
4. Sau khi cải thiện, tạo nội dung report-ready cho Word report theo khung 12 mục.
5. Tạo checklist cuối cho source code, report, slide, demo.
6. Nhấn mạnh yêu cầu thêm comment tiếng Việt trong source code: comment ngắn gọn, giải thích logic quan trọng, không đổi hành vi chương trình, không ghi secret.

Không được bịa tính năng hoặc kết quả. Nếu thiếu thông tin thành viên, screenshot, slide hoặc citation dataset thì đánh dấu Need confirmation hoặc Not found in current project.
```

## 10. Prompt hoàn chỉnh để đưa lại vào Codex thực hiện cải thiện đồ án

```text
You are working inside the root folder of the current project. Read PROJECT_IMPROVEMENT_PLAN.md first, then inspect the repository before editing.

Goal: improve the Data Mining course project according to rubric priority without breaking existing features.

Requirements:
- Improve documentation needed for the final Word report and PowerPoint slides.
- Add or improve concise Vietnamese comments in important source code sections.
- Improve data analysis evidence and report-friendly explanation files.
- Improve model/evaluation evidence if simple and safe.
- Improve API/frontend evidence and demo guide.
- Improve README and run guide.
- Do not expose secrets or credentials.
- Do not invent features, metrics, or team members.
- Run safe verification commands after edits when possible.
- Create a final summary file named FINAL_PROJECT_COMPLETION_SUMMARY.md.

Safe implementation order:
1. Backup/inspect project: check git status, read PROJECT_IMPROVEMENT_PLAN.md, read key files.
2. Improve documentation: docs/data-analysis.md, docs/model-training.md, docs/system-design.md, docs/demo-guide.md, docs/teamwork.md if evidence exists.
3. Improve data analysis evidence: ensure audit, Pearson table, figures, feature scenarios table are documented.
4. Improve model/evaluation evidence: ensure model metrics, comparison, coefficients are easy to report.
5. Improve API/frontend evidence: ensure API spec, frontend flow, DB history are documented.
6. Add detailed comments: Python scripts, FastAPI endpoints/services, C# controller/services, JS API call, Docker compose.
7. Improve README and demo guide: commands for backend, frontend, Docker, tests.
8. Run verification commands: build_dataset, train_model, evaluate_model, compare_models, pytest ml-service/tests, dotnet build.
9. Write FINAL_PROJECT_COMPLETION_SUMMARY.md with changed files, verification results, remaining risks.

Keep the code simple and suitable for students. Do not over-engineer.
```

## 11. Checklist ưu tiên hoàn thiện đồ án

| STT | Việc cần làm | Ưu tiên | Người/phần phụ trách đề xuất | Kết quả mong đợi | Minh chứng sau khi hoàn thành |
| --- | --- | --- | --- | --- | --- |
| 1 | Chuẩn hóa README và hướng dẫn chạy | P0 | Documentation/DevOps | README đọc rõ, chạy theo được | `README.md` |
| 2 | Bổ sung teamwork docs | P0 | Nhóm trưởng/All members | Có phân công và minh chứng | `docs/teamwork.md`, git commits |
| 3 | Tạo data analysis doc | P0 | Data member | Báo cáo phần dữ liệu đủ chứng cứ | `docs/data-analysis.md` |
| 4 | Tạo model training doc | P0 | ML member | Giải thích model/scenario/metrics rõ | `docs/model-training.md` |
| 5 | Tạo demo guide và screenshot checklist | P0 | Frontend/DevOps | Biết cần chụp gì cho report/slide | `docs/demo-guide.md`, `docs/screenshots/README.md` |
| 6 | Thêm comment tiếng Việt vào code quan trọng | P0 | All devs | Source dễ giải thích khi bảo vệ | Python/C#/JS files |
| 7 | Chụp ảnh giao diện, Swagger, Docker | P0 | Frontend/Presenter | Có hình minh chứng báo cáo | `docs/screenshots/` hoặc `reports/figures/` |
| 8 | Tạo sơ đồ kiến trúc và luồng dự đoán | P1 | System design | Báo cáo trực quan hơn | `reports/figures/architecture_diagram.png`, `prediction_flow.png` |
| 9 | Tạo bảng CSV feature scenarios/model metrics | P1 | ML/Data | Dễ copy vào Word/slide | `reports/tables/feature_scenarios.csv`, `model_metrics.csv` |
| 10 | Kiểm tra HTML validation khớp backend | P1 | Frontend | Form ít lỗi biên hơn | `Views/Home/Index.cshtml` |
| 11 | Kiểm tra Docker end-to-end | P1 | DevOps | Demo chạy ổn bằng Docker | Screenshot/log Docker |
| 12 | Thêm model so sánh đơn giản nếu còn thời gian | P2 | ML member | Có thêm chiều sâu mô hình | `scripts/compare_models.py` |
| 13 | Thêm test/manual case cho frontend | P2 | QA/Frontend | Demo có checklist rõ | `tests/manual/` |

## 12. Kết luận đánh giá nhanh

Project hiện đã ở mức **khá sẵn sàng về source code và chức năng cốt lõi**: có dữ liệu, preprocessing, phân tích Pearson, mô hình hồi quy, đánh giá, backend API, frontend MVC, lưu lịch sử MySQL, Docker và test backend. Các bằng chứng chính nằm ở `scripts/`, `ml-service/`, `webapp/`, `database/`, `reports/` và `REPORT_SOURCE_MATERIAL.md`.

Rủi ro lớn nhất trước khi nộp là phần báo cáo và minh chứng: chưa thấy PowerPoint, chưa có screenshot demo, chưa có file phân công thành viên rõ, README có dấu hiệu lỗi encoding, và chưa có tài liệu phân tích/model riêng đủ đẹp để đưa vào Word. Ngoài ra, `web_minimal` có R² thấp nên cần giải thích hạn chế và lý do vẫn dùng trong app do form nhập liệu đơn giản.

Việc nên làm đầu tiên là: cập nhật README, tạo `docs/teamwork.md`, tạo `docs/data-analysis.md`, tạo `docs/model-training.md`, tạo `docs/demo-guide.md`, chụp ảnh demo, và bổ sung comment tiếng Việt vào các đoạn code chính. Sau đó chạy lại các lệnh kiểm tra và viết `FINAL_PROJECT_COMPLETION_SUMMARY.md`.

## Commands đã chạy trong lần phân tích này

| Lệnh | Kết quả tóm tắt |
| --- | --- |
| `git status --short` | Chỉ thấy `REPORT_SOURCE_MATERIAL.md` đang untracked tại thời điểm kiểm tra |
| `git log --oneline --all --decorate -n 30` | Có commit history từ `first commit` đến `fix error`, đủ để tham khảo tiến độ nhưng chưa đủ mapping thành viên |
| `rg --files` | Liệt kê cấu trúc project, xác nhận có backend/frontend/data/reports/docs/tests |
| `Get-Content REPORT_SOURCE_MATERIAL.md -TotalCount 80` | Xác nhận tài liệu nguồn báo cáo đã tồn tại |

## Lưu ý bảo mật

`docker-compose.yml` và `appsettings.json` có cấu hình kết nối database. Khi đưa vào báo cáo hoặc slide, không ghi mật khẩu thật; chỉ dùng mô tả hoặc `[SECRET DETECTED - DO NOT INCLUDE]`.
