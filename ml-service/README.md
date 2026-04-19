# Backend Python - Predict the score

## 1. Mục đích

Backend Python trong dự án **Predict the score** được xây dựng bằng **FastAPI** và có nhiệm vụ chính là:

- nhận dữ liệu đầu vào từ frontend ASP.NET Core MVC
- kiểm tra và chuẩn hóa dữ liệu đầu vào
- nạp mô hình học máy đã huấn luyện
- thực hiện suy luận để dự đoán điểm số
- trả kết quả dự đoán về frontend dưới dạng JSON
- hỗ trợ kiểm thử độc lập qua Swagger, curl hoặc test script

Backend được tách riêng khỏi frontend để dễ bảo trì, dễ kiểm thử và thuận tiện mở rộng khi thay đổi mô hình hoặc logic tiền xử lý.

---

## 2. Vai trò của backend trong toàn hệ thống

Hệ thống gồm 2 phần:

- **Frontend ASP.NET Core MVC**: hiển thị giao diện, nhận dữ liệu người dùng nhập, gửi request đến backend và hiển thị kết quả
- **Backend Python FastAPI**: xử lý dữ liệu, gọi mô hình học máy và trả kết quả dự đoán

### Luồng hoạt động

1. Người dùng nhập dữ liệu trên form web
2. Frontend gửi dữ liệu tới endpoint `/predict`
3. Backend nhận request và kiểm tra dữ liệu theo schema
4. Backend tiền xử lý dữ liệu theo đúng logic mô hình
5. Backend nạp model đã train từ thư mục `artifacts/`
6. Backend sinh ra điểm dự đoán
7. Backend trả JSON kết quả về frontend
8. Frontend hiển thị kết quả cho người dùng

---

## 3. Cấu trúc thư mục backend

```text
ml-service/
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── request.py
│   │   └── response.py
│   ├── services/
│   │   ├── model_loader.py
│   │   ├── predictor.py
│   │   └── preprocessing.py
│   └── utils/
│       └── logger.py
├── artifacts/
│   ├── .gitkeep
│   ├── model.joblib
│   └── feature_config.json
└── tests/
    └── test_predict_api.py
```

---

## 4. Mô tả chi tiết từng file và thư mục

### `requirements.txt`
Chứa danh sách thư viện Python cần dùng cho backend, ví dụ:

- fastapi
- uvicorn
- pydantic
- scikit-learn
- pandas
- joblib

### `app/main.py`
Là điểm khởi động chính của FastAPI.

Nhiệm vụ:
- tạo đối tượng `FastAPI`
- khai báo endpoint gốc `/`
- khai báo endpoint dự đoán `/predict`
- liên kết request schema, response schema và logic dự đoán

### `app/schemas/request.py`
Khai báo cấu trúc dữ liệu đầu vào mà API chấp nhận.

Ví dụ các trường đầu vào hiện tại có thể bao gồm:
- `studytime`
- `failures`
- `absences`
- `schoolsup`
- `famsup`
- `internet`

File này giúp backend:
- kiểm tra dữ liệu đầu vào có đủ trường hay không
- kiểm tra kiểu dữ liệu
- từ chối request sai format ngay từ đầu

### `app/schemas/response.py`
Khai báo cấu trúc dữ liệu đầu ra mà backend trả về.

Ví dụ:
- `predicted_score`
- `model_name`

File này giúp frontend và backend thống nhất định dạng JSON trả về.

### `app/services/model_loader.py`
Phụ trách nạp mô hình từ thư mục `artifacts/`.

Nhiệm vụ:
- tìm file model
- đọc model bằng `joblib`
- kiểm tra model có tồn tại hay không
- xử lý lỗi nếu thiếu model

### `app/services/preprocessing.py`
Chứa logic tiền xử lý dữ liệu đầu vào trước khi đưa vào mô hình.

Nhiệm vụ:
- chuyển dữ liệu request thành đúng thứ tự feature
- đổi biến nhị phân sang số nếu cần
- chuẩn hóa dữ liệu theo logic đã dùng lúc train
- bảo đảm dữ liệu lúc suy luận khớp với dữ liệu lúc huấn luyện

### `app/services/predictor.py`
Là lớp trung gian gọi model để dự đoán.

Nhiệm vụ:
- nhận dữ liệu đã tiền xử lý
- gọi `model.predict(...)`
- lấy ra kết quả
- ép kiểu kết quả sang `float` nếu cần
- trả kết quả về cho `main.py`

### `app/utils/logger.py`
Dùng để hỗ trợ log hệ thống.

Có thể dùng để:
- log request
- log lỗi thiếu model
- log lỗi dữ liệu đầu vào
- log thời gian xử lý

### `artifacts/`
Chứa file model sau khi train.

Ví dụ:
- `model.joblib`
- `feature_config.json`

Đây là nơi backend đọc model để dự đoán.

### `tests/test_predict_api.py`
Chứa test cho endpoint `/predict`.

Dùng để kiểm tra:
- API có chạy không
- request hợp lệ có trả về kết quả không
- request sai dữ liệu có bị từ chối đúng không

---

## 5. Backend liên hệ với các file trong `scripts/` như thế nào

Các file trong `scripts/` **không chạy cùng frontend khi runtime**, nhưng chúng tạo đầu ra để backend sử dụng.

### `scripts/download_data.py`
Tải bộ dữ liệu Student Performance từ UCI và giải nén vào `data/raw/`.

### `scripts/build_dataset.py`
Đọc dữ liệu gốc từ `data/raw/`, làm sạch dữ liệu, sinh:
- `data/processed/student_performance_clean.csv`
- `data/processed/feature_config.json`
- `reports/processing_audit.json`
- `reports/tables/pearson_correlation.csv`
- các hình trong `reports/figures/`

### `scripts/train_model.py`
Huấn luyện mô hình và lưu file model vào:
- `ml-service/artifacts/model.joblib`

### `scripts/evaluate_model.py`
Đánh giá mô hình, xuất metrics và hình minh họa.

### `scripts/export_sample_input.py`
Sinh file:
- `data/samples/sample_input.csv`

### Kết luận quan hệ
`scripts/` chạy **độc lập**, nhưng backend **dùng đầu ra của chúng** để suy luận.

Luồng đúng là:

```text
scripts/ -> data/processed + ml-service/artifacts -> backend FastAPI -> frontend ASP.NET MVC
```

---

## 6. Yêu cầu môi trường

Trước khi chạy backend, cần có:

- Python 3.10 trở lên
- pip
- môi trường ảo `.venv`
- các thư viện được cài trong `requirements.txt`

---

## 7. Khởi động backend

### Bước 1: đi tới thư mục backend

```bash
cd /d/StudyMaterials/HK6/DataMining/Groups/Project/Predict_the_score/ml-service
```

### Bước 2: tạo môi trường ảo nếu chưa có

```bash
python -m venv .venv
```

### Bước 3: kích hoạt môi trường ảo

```bash
source .venv/Scripts/activate
```

### Bước 4: cài thư viện

```bash
python -m pip install --upgrade pip
pip install fastapi "uvicorn[standard]" pydantic scikit-learn pandas joblib
```

Hoặc nếu đã có `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Bước 5: chạy backend

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## 8. Kiểm tra sau khi chạy

Nếu backend chạy thành công, hệ thống sẽ có:

- API gốc: `http://127.0.0.1:8000`
- Swagger Docs: `http://127.0.0.1:8000/docs`

### Endpoint gốc

`GET /`

Mục đích:
- kiểm tra service có đang chạy hay không

Ví dụ response:

```json
{
  "message": "ML service is running"
}
```

### Endpoint dự đoán

`POST /predict`

Mục đích:
- nhận dữ liệu đầu vào
- trả về điểm dự đoán

Ví dụ request:

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

Ví dụ response:

```json
{
  "predicted_score": 12.5,
  "model_name": "baseline-demo"
}
```

---

## 9. Mẫu code tối thiểu

### `app/main.py`

```python
from fastapi import FastAPI
from app.schemas.request import PredictionRequest
from app.schemas.response import PredictionResponse

app = FastAPI(title="Predict The Score API")

@app.get("/")
def root():
    return {"message": "ML service is running"}

@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
    predicted_score = 12.5
    return PredictionResponse(
        predicted_score=predicted_score,
        model_name="baseline-demo"
    )
```

### `app/schemas/request.py`

```python
from pydantic import BaseModel

class PredictionRequest(BaseModel):
    studytime: int
    failures: int
    absences: int
    schoolsup: int
    famsup: int
    internet: int
```

### `app/schemas/response.py`

```python
from pydantic import BaseModel

class PredictionResponse(BaseModel):
    predicted_score: float
    model_name: str
```

---

## 10. Cách tích hợp model thật

Khi hoàn thành huấn luyện mô hình, backend cần đổi từ bản demo sang bản đọc model thật.

### Bước tích hợp

1. huấn luyện model bằng `scripts/train_model.py`
2. lưu model vào `ml-service/artifacts/model.joblib`
3. lưu file mô tả feature vào `ml-service/artifacts/feature_config.json`
4. viết `model_loader.py` để nạp model
5. viết `preprocessing.py` để chuẩn hóa dữ liệu đầu vào
6. viết `predictor.py` để gọi model dự đoán
7. thay logic hard-code trong `main.py` bằng logic gọi predictor

---

## 11. Nguyên tắc viết backend

Backend cần tuân theo các nguyên tắc sau:

- schema đầu vào và đầu ra phải rõ ràng
- dữ liệu đầu vào phải được validate
- logic tiền xử lý khi predict phải giống logic khi train
- model phải được nạp từ file artifact, không hard-code trong source
- lỗi phải được thông báo rõ
- code nên tách file theo chức năng, không dồn toàn bộ vào `main.py`

---

## 12. Kiểm thử backend

Có 3 cách kiểm thử chính:

### Cách 1: Swagger
Mở:
`http://127.0.0.1:8000/docs`

Tại đây có thể:
- xem schema request/response
- gửi thử request trực tiếp
- kiểm tra JSON trả về

### Cách 2: curl

```bash
curl -X POST "http://127.0.0.1:8000/predict" ^
  -H "Content-Type: application/json" ^
  -d "{\"studytime\":2,\"failures\":0,\"absences\":4,\"schoolsup\":1,\"famsup\":1,\"internet\":1}"
```

### Cách 3: test script
Tạo test trong `tests/test_predict_api.py` để kiểm tra tự động.

---

## 13. Các lỗi thường gặp và cách xử lý

### Lỗi: `fastapi: command not found`
Nguyên nhân:
- chưa cài FastAPI CLI hoặc môi trường ảo chưa kích hoạt

Cách xử lý:
- kích hoạt `.venv`
- chạy bằng `python -m uvicorn ...`

### Lỗi: `ImportError: cannot import name 'PredictionRequest'`
Nguyên nhân:
- file `request.py` chưa có class `PredictionRequest`
- tên class không khớp
- file chưa lưu

Cách xử lý:
- kiểm tra lại `app/schemas/request.py`

### Lỗi: `Could not import module "app.main"`
Nguyên nhân:
- sai cấu trúc thư mục
- thiếu `__init__.py`
- file `main.py` lỗi cú pháp

Cách xử lý:
- kiểm tra lại cấu trúc package
- thêm `__init__.py` nếu cần
- chạy lại sau khi sửa lỗi import

### Lỗi: backend chạy nhưng frontend không gọi được
Nguyên nhân:
- backend chưa chạy
- sai URL API trong frontend
- sai schema request/response

Cách xử lý:
- kiểm tra backend ở `/docs`
- kiểm tra cấu hình URL trong webapp
- kiểm tra dữ liệu frontend gửi đi

---

## 14. Đầu ra mong đợi của backend

Sau khi hoàn thiện, backend Python phải đạt các kết quả sau:

- chạy được độc lập bằng Uvicorn
- có endpoint `/predict`
- nhận request đúng schema
- trả JSON đúng schema
- đọc được model từ `artifacts/`
- xử lý được dữ liệu đầu vào
- có log và thông báo lỗi cơ bản
- sẵn sàng để frontend ASP.NET Core MVC gọi tới

---

## 15. Tóm tắt nhiệm vụ backend

Backend Python chịu trách nhiệm cho toàn bộ phần suy luận mô hình của hệ thống. Đây là nơi kết nối giữa dữ liệu đầu vào người dùng và mô hình học máy. Nếu frontend là phần giao tiếp với người dùng, thì backend chính là phần xử lý logic dự đoán cốt lõi của dự án.

Nói ngắn gọn:

- frontend gửi dữ liệu
- backend xử lý
- model dự đoán
- backend trả kết quả
- frontend hiển thị

---

## 16. Gợi ý phát triển tiếp

Trong các bước tiếp theo, backend có thể được mở rộng thêm:

- endpoint health check
- endpoint lưu lịch sử dự đoán
- middleware log request/response
- validate dữ liệu chặt hơn
- hỗ trợ nhiều phiên bản model
- tách config ra file riêng
- thêm test tự động cho nhiều trường hợp lỗi
