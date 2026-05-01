from fastapi import FastAPI
from app.schemas.request import PredictionRequest
from app.schemas.response import PredictionResponse
from app.services.model_loader import load_model_bundle
from app.services.predictor import predict_score

app = FastAPI(title="Predict The Score API")

@app.on_event("startup")
def startup_load_model():
    load_model_bundle()

@app.get("/")
def root():
    return {"message": "Machine Learning is running"}

@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
    predicted_score = predict_score(payload)
    return PredictionResponse(
        predicted_score=predicted_score,
        model_name="linear-regression-web-minimal"
    )