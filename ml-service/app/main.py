from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.schemas.request import PredictionRequest
from app.schemas.response import ModelInfoResponse, PredictionResponse
from app.services.model_loader import get_model_info, load_model_bundle
from app.services.predictor import predict_score

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        load_model_bundle("web_minimal")
    except FileNotFoundError:
        # Cho phép /health vẫn chạy dù nhóm chưa train model.joblib.
        pass
    yield


app = FastAPI(
    title="Predict The Score API",
    description="FastAPI service that predicts the final student score G3 from web form inputs.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {"message": "Machine Learning API is running"}


@app.get("/health")
def health():
    """Endpoint kiểm tra backend và trạng thái nạp model."""
    try:
        load_model_bundle("web_minimal")
        return {"status": "ok", "model_loaded": True}
    except FileNotFoundError:
        return {"status": "ok", "model_loaded": False}


@app.get("/model-info", response_model=ModelInfoResponse)
def model_info():
    """Trả metadata của model để Swagger và báo cáo dễ kiểm chứng."""
    return get_model_info()


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
    """Dự đoán điểm G3 thang 20 và quy đổi sang thang 10 cho frontend."""
    try:
        predicted_score = round(predict_score(payload), 2)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    predicted_score_10 = round(predicted_score / 2, 2)
    model_bundle = load_model_bundle(payload.scenario)
    model_scenario = model_bundle.get("scenario", payload.scenario)
    model_name = model_bundle.get("model_name", "LinearRegression")

    return PredictionResponse(
        predicted_score=predicted_score,
        predicted_score_20=predicted_score,
        predicted_score_10=predicted_score_10,
        model_name=f"{model_name}-{model_scenario}",
        scenario=payload.scenario,
        model_scenario=model_scenario,
        message="Dự đoán thành công.",
    )
