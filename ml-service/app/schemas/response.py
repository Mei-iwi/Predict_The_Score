from pydantic import BaseModel

class PredictionResponse(BaseModel):
    predicted_score: float
    model_name: str