from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


ScenarioName = Literal["web_minimal", "early_warning", "reference"]


class PredictionRequest(BaseModel):
    """Input cho /predict; scenario thiếu sẽ tự dùng web_minimal để tương thích API cũ."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "scenario": "web_minimal",
                "studytime": 2,
                "failures": 0,
                "absences": 4,
                "schoolsup": 1,
                "famsup": 1,
                "internet": 1,
            }
        }
    )

    scenario: ScenarioName = Field("web_minimal", description="Prediction scenario: web_minimal, early_warning, or reference.")
    studytime: int = Field(..., ge=1, le=4, description="Weekly study time level from 1 to 4.")
    failures: int = Field(..., ge=0, le=4, description="Number of previous class failures from 0 to 4.")
    absences: int = Field(..., ge=0, le=93, description="Number of school absences from 0 to 93.")
    schoolsup: int = Field(..., ge=0, le=1, description="Extra school support: 1 for yes, 0 for no.")
    famsup: int = Field(..., ge=0, le=1, description="Family educational support: 1 for yes, 0 for no.")
    internet: int = Field(..., ge=0, le=1, description="Internet access at home: 1 for yes, 0 for no.")
    subject: Literal["mat", "por"] | None = Field(None, description="Subject: mat for Math, por for Portuguese.")
    higher: int | None = Field(None, ge=0, le=1, description="Wants to take higher education: 1 for yes, 0 for no.")
    traveltime: int | None = Field(None, ge=1, le=4, description="Home to school travel time from 1 to 4.")
    G1: int | None = Field(None, ge=0, le=20, description="First period grade from 0 to 20.")
    G2: int | None = Field(None, ge=0, le=20, description="Second period grade from 0 to 20.")

    @model_validator(mode="after")
    def validate_scenario_fields(self) -> "PredictionRequest":
        """Kiểm tra field bắt buộc theo từng kịch bản để FastAPI trả lỗi 422 rõ ràng."""
        required_by_scenario = {
            "web_minimal": [],
            "early_warning": ["subject", "higher", "traveltime"],
            "reference": ["subject", "higher", "traveltime", "G1", "G2"],
        }
        missing = [name for name in required_by_scenario[self.scenario] if getattr(self, name) is None]
        if missing:
            raise ValueError(f"Scenario '{self.scenario}' thiếu field bắt buộc: {missing}")
        return self
