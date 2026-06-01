# Final project completion summary

## Đã hoàn thiện

- Chuẩn hóa `README.md` với hướng dẫn chạy data pipeline, backend, frontend, Docker và test.
- Bổ sung tài liệu phục vụ báo cáo:
  - `docs/project-overview.md`
  - `docs/data-analysis.md`
  - `docs/model-training.md`
  - `docs/system-design.md`
  - `docs/api-spec.md`
  - `docs/demo-guide.md`
  - `docs/teamwork.md`
  - `docs/report-evidence.md`
  - `docs/screenshots/README.md`
- Bổ sung tài liệu nộp bài:
  - `REPORT_SOURCE_MATERIAL_UPDATED.md`
  - `SLIDE_CONTENT.md`
  - `SUBMISSION_CHECKLIST.md`
- Bổ sung bảng và sơ đồ phục vụ report/slide:
  - `reports/tables/feature_scenarios.csv`
  - `reports/tables/model_metrics.csv`
  - `reports/figures/architecture_diagram.mmd`
  - `reports/figures/prediction_flow.mmd`
- Thêm comment tiếng Việt ngắn gọn vào các phần quan trọng của pipeline ML, FastAPI, MVC, service lưu history và JavaScript.
- Sửa validation HTML để khớp backend:
  - `absences`: `0-93`
  - `failures`: `0-4`
- Pin lại dependency trong `ml-service/requirements.txt` và bỏ `jupyter/notebook` khỏi requirements backend để giảm dependency không cần cho API/test.

## Kết quả kiểm thử đã chạy

| Lệnh | Kết quả |
| --- | --- |
| `dotnet build webapp/PredictTheScore.Web/PredictTheScore.Web.csproj` | Pass khi chạy ngoài sandbox, 0 warning, 0 error |
| `dotnet build webapp/PredictTheScore.Web/PredictTheScore.Web.csproj --no-restore` | Pass, 0 warning, 0 error |
| Python AST parse cho `scripts/*.py` và `ml-service/app/**/*.py` | Pass, parse 13 file Python thành công |
| Parse JSON reports | Pass |
| Parse CSV reports | Pass |

## Lệnh chưa chạy được trong môi trường hiện tại

| Lệnh | Lý do |
| --- | --- |
| `python scripts/build_dataset.py` | Python hiện tại thiếu `matplotlib` và các package project |
| `python scripts/train_model.py --scenario web_minimal` | Chưa cài được dependency Python |
| `python scripts/evaluate_model.py` | Chưa cài được dependency Python |
| `python scripts/compare_models.py` | Chưa cài được dependency Python |
| `pytest ml-service/tests` | Python hiện tại thiếu `pytest`, `fastapi`, `pandas`, `scikit-learn` |
| `docker compose build ml-service` | Docker Desktop engine chưa chạy: không tìm thấy `dockerDesktopLinuxEngine` |

## Ghi chú môi trường

- Interpreter trong sandbox là `C:\msys64\ucrt64\bin\python.exe`.
- Interpreter này không có các package Python của project.
- Thử cài dependency bằng pip vào `.codex_pydeps` bị lỗi vì MSYS2 Python không dùng wheel Windows chuẩn cho `pandas/numpy` và quá trình build dependency bị lỗi SSL khi tải build tool.
- Trên máy demo nên dùng Python chính thức từ python.org hoặc Docker Desktop đang chạy, sau đó cài `ml-service/requirements.txt`.

## Các phần nhóm cần bổ sung thủ công

- Điền tên thành viên và commit evidence trong `docs/teamwork.md`.
- Chụp screenshot demo theo `docs/screenshots/README.md`.
- Tạo file PowerPoint từ `SLIDE_CONTENT.md`.
- Biên tập Word report từ `REPORT_SOURCE_MATERIAL_UPDATED.md` và các docs trong `docs/`.
- Không đưa mật khẩu database thật từ cấu hình local/Docker vào báo cáo hoặc slide.

