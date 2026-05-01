# Predict the score

Ứng dụng dự đoán điểm số học sinh với kiến trúc tách thành 2 phần:

- **Frontend:** ASP.NET Core MVC
- **Backend:** Python FastAPI

---

## Mục lục

- [Khởi động dự án](#khởi-động-dự-án)
- [Giới thiệu dự án](#giới-thiệu-dự-án)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Mô tả cấu trúc thư mục](#mô-tả-cấu-trúc-thư-mục)
- [Quy trình chạy hệ thống](#quy-trình-chạy-hệ-thống)
- [Ghi chú](#ghi-chú)

---

## Khởi động dự án

### Cài môi trường ảo và thư viện

Mở git bash hoặc terminal trong dự án

Di chuyển vào backend ml-service

```bash
cd ml-service
```

Kích hoạt môi trường ảo: -> Chỉ chạy cho lần đầu

```bash 
python -m venv .venv
```

Cài đặt thư viện cần thiết: -> Chỉ chạy cho lần đầu

```bash
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Dữ liệu và tiền xử lý dữ liệu

Tải dữ liệu student Performance từ UCI, lưu vào data/raw/student.zip, kiểm tra và giải nén dữ liệu gốc

```bash
python scripts/download_data.py
```

Đọc student-mat.csv, student-por.csv, chọn cột, mã hóa yes/no thành 1/0, làm sạch dữ liệu, tạo student_performance_clean.csv, feature_config.json, audit và biểu đồ Pearson

```bash
python scripts/build_dataset.py 
```

Đọc dữ liệu sạch, lấy scenario web_minimal, train mô hình LinearRegression, lưu model vào ml-service/artifacts/model.joblib, lưu metrics

```bash
python scripts/train_model.py 
```
Nạp lại model.joblib, đánh giá model trên test set, tạo file evaluation và hình actual_vs_predicted

```bash
python scripts/evaluate_model.py
```

Tạo dữ liệu mẫu sample_input.csv và sample_input.json theo schema web hiện tại

```bash
python scripts/export_sample_input.py 
```

### Khởi động và tạo CSDL (mysql bằng docker)

Chạy docker
```bash
docker compose up --build
```

Ngắt docker (-v xóa ổ đĩa lưu trữ)
```bash
docker compose down -v
```

Sử dụng một trình giao diện (wordbench, xml, ...) để truy cập csdl trực quan
```bash
hosetname: 127.0.0.1 
port: 3306
User: root
Password: root_password

User: predict_user
Password: predict_password
```


> Chạy **Backend trước**, sau đó mới chạy **Frontend**.

### 1) Backend - FastAPI

Di chuyển tới thư mục `ml-service`:

```bash
cd ml-service
```

Chạy backend:

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Sau khi chạy thành công:

- **API:** `http://127.0.0.1:8000`
- **Swagger Docs:** `http://127.0.0.1:8000/docs`

---

### 2) Frontend - ASP.NET Core MVC

Di chuyển tới thư mục project web:

```bash
cd PredictTheScore.Web
```

Chạy dự án:

```bash
dotnet run
```

Hoặc chạy ở chế độ tự theo dõi thay đổi:

```bash
dotnet watch run
```

---

## Giới thiệu dự án

**Predict the score** là dự án xây dựng ứng dụng dự đoán điểm số học sinh.

Hệ thống được chia thành 2 phần:

- **Frontend ASP.NET Core MVC**: hiển thị giao diện, nhận dữ liệu người dùng nhập và trả kết quả dự đoán.
- **Backend FastAPI**: nhận request từ frontend, xử lý dữ liệu đầu vào, gọi mô hình học máy và trả kết quả dự đoán qua API.

---

## Công nghệ sử dụng

### Frontend
- ASP.NET Core MVC
- Razor View
- CSS
- JavaScript

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic
- scikit-learn
- pandas
- joblib

---

## Cấu trúc thư mục

```text
Predict_the_score/
├── README.md
├── .gitignore
├── docs/
│   ├── README.md
│   ├── progress/
│   │   ├── week-01.md
│   │   ├── week-02.md
│   │   └── week-03.md
│   ├── architecture/
│   │   └── architecture-overview.md
│   ├── api/
│   │   └── predict-api.md
│   └── database/
│       └── schema-note.md
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── samples/
├── notebooks/
│   ├── 01_profiling.ipynb
│   ├── 02_preprocessing.ipynb
│   └── 03_modeling.ipynb
├── scripts/
│   ├── download_data.py
│   ├── build_dataset.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   └── export_sample_input.py
├── ml-service/
│   ├── README.md
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── schemas/
│   │   │   ├── request.py
│   │   │   └── response.py
│   │   ├── services/
│   │   │   ├── model_loader.py
│   │   │   ├── predictor.py
│   │   │   └── preprocessing.py
│   │   └── utils/
│   │       └── logger.py
│   ├── artifacts/
│   └── tests/
│       └── test_predict_api.py
├── webapp/
│   └── PredictTheScore.Web/
│       ├── Controllers/
│       ├── Models/
│       ├── ViewModels/
│       ├── Services/
│       ├── Views/
│       ├── wwwroot/
│       ├── appsettings.json
│       ├── Program.cs
│       └── PredictTheScore.Web.csproj
├── database/
│   ├── schema/
│   ├── seed/
│   └── migrations/
├── tests/
│   ├── integration/
│   └── manual/
└── reports/
    ├── figures/
    ├── tables/
    └── README.md
```

---

## Mô tả cấu trúc thư mục

### `docs/`
Chứa tài liệu mô tả dự án, tiến độ thực hiện, kiến trúc hệ thống, tài liệu API và ghi chú cơ sở dữ liệu.

### `data/`
Chứa dữ liệu sử dụng trong quá trình làm đồ án:

- `raw/`: dữ liệu gốc
- `interim/`: dữ liệu trung gian sau xử lý bước đầu
- `processed/`: dữ liệu sạch dùng để train/test
- `samples/`: dữ liệu mẫu phục vụ test nhanh

### `notebooks/`
Chứa các notebook phân tích dữ liệu, tiền xử lý và thử nghiệm mô hình.

### `scripts/`
Chứa các script để tự động hóa các bước xử lý dữ liệu, huấn luyện mô hình và đánh giá mô hình.

### `ml-service/`
Chứa backend Python FastAPI:

- `app/main.py`: file khởi động API
- `schemas/`: định nghĩa request/response
- `services/`: xử lý nạp mô hình, tiền xử lý và dự đoán
- `utils/`: tiện ích hỗ trợ như logger
- `artifacts/`: nơi lưu model đã train
- `tests/`: kiểm thử cho backend

### `webapp/PredictTheScore.Web/`
Chứa frontend ASP.NET Core MVC:

- `Controllers/`: xử lý request từ người dùng
- `Models/`: mô hình dữ liệu
- `ViewModels/`: dữ liệu trung gian giữa controller và view
- `Services/`: lớp gọi API backend
- `Views/`: giao diện hiển thị
- `wwwroot/`: CSS, JavaScript, hình ảnh tĩnh
- `Program.cs`: file cấu hình khởi động ứng dụng

### `database/`
Chứa tài liệu hoặc script liên quan đến thiết kế cơ sở dữ liệu:

- `schema/`: script khởi tạo bảng
- `seed/`: dữ liệu mẫu
- `migrations/`: thay đổi cấu trúc CSDL

### `tests/`
Chứa các tài liệu và kịch bản kiểm thử tích hợp, kiểm thử thủ công.

### `reports/`
Chứa hình ảnh, bảng biểu và tài liệu phục vụ báo cáo, slide và minh họa kết quả.

---

## Quy trình chạy hệ thống

1. Chạy backend FastAPI.
2. Kiểm tra backend hoạt động qua `/docs`.
3. Chạy frontend ASP.NET Core MVC.
4. Truy cập giao diện web.
5. Nhập dữ liệu đầu vào.
6. Frontend gửi dữ liệu sang backend để dự đoán.
7. Backend trả kết quả dự đoán về frontend để hiển thị.

---

## Ghi chú

- Nếu backend chưa chạy, frontend sẽ không lấy được kết quả dự đoán.
- Nếu thay đổi schema request/response bên backend, cần cập nhật lại phần gọi API bên frontend.
- Các file model sau khi train nên lưu trong thư mục `ml-service/artifacts/`.

---

## Trạng thái hiện tại

Dự án đang được xây dựng theo lộ trình:

- hoàn thiện backend dự đoán
- hoàn thiện frontend nhập liệu và hiển thị kết quả
- tích hợp hai hệ thống
- kiểm thử và đóng gói báo cáo
