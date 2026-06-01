# Predict The Score

Ứng dụng dự đoán điểm cuối kỳ `G3` của học sinh bằng mô hình hồi quy tuyến tính. Project dùng dữ liệu UCI Student Performance, backend FastAPI, frontend ASP.NET Core MVC và MySQL để lưu lịch sử dự đoán.

## 1. Lưu ý trước khi chạy

Luôn mở terminal tại **thư mục gốc của project**. Thư mục gốc là thư mục chứa các file/thư mục sau:

```text
ml-service/
webapp/
scripts/
data/
reports/
docker-compose.yml
README.md
```

Kiểm tra nhanh đang ở đúng thư mục gốc:

```bash
ls
```

Nếu thấy `ml-service`, `webapp`, `scripts`, `data`, `reports`, `docker-compose.yml` thì đúng.

Các lỗi thường gặp:

- Nếu đang ở thư mục gốc thì mới chạy `cd ml-service`.
- Nếu đã ở trong `ml-service` rồi thì **không chạy lại** `cd ml-service`, vì sẽ bị lỗi `No such file or directory`.
- Trong Git Bash, lệnh kiểu Windows `.\.venv\Scripts\activate` là sai.
- Trong Git Bash, dùng `source .venv/Scripts/activate` nếu đang ở `ml-service`.
- Trong Git Bash, dùng `source ml-service/.venv/Scripts/activate` nếu đang ở thư mục gốc.
- Trong PowerShell, dùng `.\.venv\Scripts\Activate.ps1`.
- Trong Command Prompt/CMD, dùng `.venv\Scripts\activate.bat`.

## 2. Kiểm tra Python trên Windows

Trên Windows có thể có `py`, `python` hoặc `python3`. Chỉ cần một lệnh chạy được là đủ.

### Git Bash

```bash
py --version
python --version
python3 --version
```

### PowerShell

```powershell
py --version
python --version
python3 --version
```

### Command Prompt / CMD

```cmd
py --version
python --version
python3 --version
```

Nếu gặp lỗi:

```text
Python was not found; run without arguments to install from the Microsoft Store...
```

hãy cài Python từ trang chính thức `https://www.python.org/downloads/windows/`. Khi cài, chọn **Add python.exe to PATH**. Sau đó đóng terminal cũ, mở terminal mới và kiểm tra lại version.

Trong README này, ví dụ dùng `py` vì đây là Python launcher phổ biến trên Windows. Nếu máy bạn không có `py` nhưng có `python`, hãy thay `py` bằng `python`.

## 3. Cài môi trường Python cho backend và scripts

Chỉ làm một lần đầu tiên, chạy từ **thư mục gốc project**.

### Cách 1: Git Bash

```bash
cd ml-service
py -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cd ..
```

Nếu lệnh `py` không chạy trong Git Bash, dùng:

```bash
cd ml-service
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cd ..
```

### Cách 2: PowerShell

```powershell
cd ml-service
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cd ..
```

Nếu PowerShell chặn activate script, chạy lệnh này rồi activate lại:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Cách 3: Command Prompt / CMD

```cmd
cd ml-service
py -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cd ..
```

## 4. Kích hoạt lại môi trường ảo sau này

Nếu đã tạo `.venv` rồi, lần sau chỉ cần activate.

### Nếu đang ở thư mục gốc project

Git Bash:

```bash
source ml-service/.venv/Scripts/activate
```

PowerShell:

```powershell
.\ml-service\.venv\Scripts\Activate.ps1
```

CMD:

```cmd
ml-service\.venv\Scripts\activate.bat
```

### Nếu đang ở thư mục `ml-service`

Git Bash:

```bash
source .venv/Scripts/activate
```

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

CMD:

```cmd
.venv\Scripts\activate.bat
```

Nếu bị lỗi `No such file or directory`, nghĩa là `.venv` chưa được tạo hoặc bạn đang đứng sai thư mục. Hãy quay về thư mục gốc và chạy lại phần cài môi trường.

## 5. Xử lý dữ liệu và huấn luyện model

Chạy từ **thư mục gốc project** sau khi đã cài thư viện Python:

### Git Bash / PowerShell / CMD

Kích hoạt môi trường ảo trước, sau đó chạy scripts từ thư mục gốc.

Git Bash:

```bash
source ml-service/.venv/Scripts/activate
python scripts/build_dataset.py
python scripts/train_model.py --scenario web_minimal
python scripts/evaluate_model.py
python scripts/compare_models.py
```

PowerShell:

```powershell
.\ml-service\.venv\Scripts\Activate.ps1
python scripts/build_dataset.py
python scripts/train_model.py --scenario web_minimal
python scripts/evaluate_model.py
python scripts/compare_models.py
```

CMD:

```cmd
ml-service\.venv\Scripts\activate.bat
python scripts/build_dataset.py
python scripts/train_model.py --scenario web_minimal
python scripts/evaluate_model.py
python scripts/compare_models.py
```

Các output quan trọng:

- `data/processed/student_performance_clean.csv`
- `reports/processing_audit.json`
- `reports/tables/pearson_correlation.csv`
- `reports/tables/model_comparison.csv`
- `reports/tables/model_coefficients.csv`
- `ml-service/artifacts/model.joblib`

## 6. Chạy backend FastAPI

Mở terminal mới, chạy từ **thư mục gốc project**.

### Git Bash

```bash
source ml-service/.venv/Scripts/activate
cd ml-service
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### PowerShell

```powershell
.\ml-service\.venv\Scripts\Activate.ps1
cd ml-service
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### CMD

```cmd
ml-service\.venv\Scripts\activate.bat
cd ml-service
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Nếu lệnh `python` không chạy sau khi activate, hãy kiểm tra lại bước tạo `.venv`.

URL kiểm tra:

- API root: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`
- Model info: `http://127.0.0.1:8000/model-info`

## 7. Chạy frontend ASP.NET Core MVC

Mở terminal khác, chạy từ **thư mục gốc project**:

```bash
cd webapp/PredictTheScore.Web
dotnet run
```

Mở URL mà `dotnet run` in ra, thường là `http://localhost:5000` hoặc `https://localhost:5001`.

Frontend gửi form đến `/Predict/Submit`, MVC controller gọi FastAPI `/predict`, sau đó lưu kết quả vào MySQL nếu database đang chạy.

## 8. Chạy bằng Docker Compose

Chạy từ **thư mục gốc project**:

```bash
docker compose up --build
```

Docker Compose có các service:

- `db`: MySQL
- `ml-service`: FastAPI backend
- `webapp`: ASP.NET Core MVC frontend

Không đưa mật khẩu thật trong file cấu hình vào báo cáo hoặc slide. Khi trình bày, chỉ mô tả là project dùng connection string local/Docker.

## 9. Kiểm thử

Chạy từ **thư mục gốc project**.

Backend tests:

Git Bash:

```bash
source ml-service/.venv/Scripts/activate
python -m pytest ml-service/tests
```

PowerShell:

```powershell
.\ml-service\.venv\Scripts\Activate.ps1
python -m pytest ml-service/tests
```

CMD:

```cmd
ml-service\.venv\Scripts\activate.bat
python -m pytest ml-service/tests
```

Build frontend:

```bash
dotnet build webapp/PredictTheScore.Web/PredictTheScore.Web.csproj
```

Checklist thủ công nằm ở `tests/manual/test_cases.md`.

## 10. API chính

Request `POST /predict`:

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

Response:

```json
{
  "predicted_score": 12.8,
  "predicted_score_10": 6.4,
  "model_name": "LinearRegression",
  "message": "Prediction completed successfully."
}
```

## 11. Xử lý lỗi thường gặp

### `bash: cd: ml-service: No such file or directory`

Bạn đang không ở thư mục gốc project hoặc đã đang ở trong `ml-service`.

Kiểm tra:

```bash
pwd
ls
```

Nếu `ls` không thấy `ml-service`, hãy `cd` về đúng thư mục chứa project.

### `bash: ..venvScriptsactivate: command not found`

Bạn đang dùng sai cú pháp activate trong Git Bash. Dùng:

```bash
source .venv/Scripts/activate
```

nếu đang ở `ml-service`, hoặc:

```bash
source ml-service/.venv/Scripts/activate
```

nếu đang ở thư mục gốc project.

### `source ml-service/.venv/Scripts/activate: No such file or directory`

Có hai khả năng:

- Bạn chưa tạo `.venv`.
- Bạn đang không ở thư mục gốc project.

Cách sửa từ thư mục gốc:

```bash
cd ml-service
py -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
cd ..
```

### `Python was not found`

Python chưa được cài hoặc chưa được thêm vào PATH. Cài Python từ `python.org`, chọn **Add python.exe to PATH**, rồi mở terminal mới.

### `ModuleNotFoundError`

Bạn chưa activate `.venv` hoặc chưa cài requirements.

Từ thư mục gốc:

```bash
source ml-service/.venv/Scripts/activate
python -m pip install -r ml-service/requirements.txt
```

Với PowerShell:

```powershell
.\ml-service\.venv\Scripts\Activate.ps1
python -m pip install -r ml-service\requirements.txt
```

## 12. Ghi chú báo cáo

- Model chính của app là `LinearRegression` với scenario `web_minimal` vì khớp 6 trường đang có trên form web.
- Scenario `reference` có độ chính xác cao hơn vì dùng thêm `G1`, `G2`, nhưng hiện form web chưa thu thập các điểm này.
- Các mục cần nhóm tự bổ sung trước khi nộp: tên thành viên thật, ảnh screenshot demo, slide PowerPoint và link commit minh chứng.
