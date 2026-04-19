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