from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PredictionResponse(BaseModel):
    """Response chính của /predict, giữ field cũ và thêm thông tin scenario."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "predicted_score": 12.8,
                "predicted_score_20": 12.8,
                "predicted_score_10": 6.4,
                "model_name": "LinearRegression-web_minimal",
                "scenario": "web_minimal",
                "model_scenario": "web_minimal",
                "message": "Prediction completed successfully.",
            }
        }
    )

    predicted_score: float = Field(..., ge=0, le=20, description="Predicted final score G3 on the 20-point scale.")
    predicted_score_20: float = Field(..., ge=0, le=20, description="Predicted final score G3 on the 20-point scale.")
    predicted_score_10: float = Field(..., ge=0, le=10, description="Predicted final score converted to the 10-point scale.")
    model_name: str = Field(..., description="Model or scenario used for prediction.")
    scenario: str = Field(..., description="Scenario requested by the client.")
    model_scenario: str = Field(..., description="Scenario stored inside the loaded model artifact.")
    message: str = Field(..., description="Short human-readable result message.")


class ModelInfoResponse(BaseModel):
    """Thông tin model đang được backend phục vụ."""

    model_name: str
    scenario: str
    feature_names: list[str]
    target: str
    metrics: dict[str, Any] | None = None
    available_scenarios: list[str] = []
    missing_scenarios: list[str] = []
