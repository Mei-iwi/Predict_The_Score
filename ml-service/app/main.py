from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.schemas.request import PredictionRequest
from app.schemas.response import ModelInfoResponse, PredictionResponse
from app.services.model_loader import get_model_info, load_model_bundle
from app.services.predictor import predict_score

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        load_model_bundle()
    except FileNotFoundError:
        # The /health endpoint should still be available before training runs.
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
    try:
        load_model_bundle()
        return {"status": "ok", "model_loaded": True}
    except FileNotFoundError:
        return {"status": "ok", "model_loaded": False}


@app.get("/model-info", response_model=ModelInfoResponse)
def model_info():
    return get_model_info()


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
    predicted_score = round(predict_score(payload), 2)
    predicted_score_10 = round(predicted_score / 2, 2)
    info = get_model_info()

    return PredictionResponse(
        predicted_score=predicted_score,
        predicted_score_10=predicted_score_10,
        model_name=info["model_name"],
        message="Prediction completed successfully.",
    )
