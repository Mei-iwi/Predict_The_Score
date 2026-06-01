from pydantic import BaseModel, ConfigDict, Field


class PredictionRequest(BaseModel):
    """Input đúng với 6 trường hiện có trên form web."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "studytime": 2,
                "failures": 0,
                "absences": 4,
                "schoolsup": 1,
                "famsup": 1,
                "internet": 1,
            }
        }
    )

    studytime: int = Field(..., ge=1, le=4, description="Weekly study time level from 1 to 4.")
    failures: int = Field(..., ge=0, le=4, description="Number of previous class failures from 0 to 4.")
    absences: int = Field(..., ge=0, le=93, description="Number of school absences from 0 to 93.")
    schoolsup: int = Field(..., ge=0, le=1, description="Extra school support: 1 for yes, 0 for no.")
    famsup: int = Field(..., ge=0, le=1, description="Family educational support: 1 for yes, 0 for no.")
    internet: int = Field(..., ge=0, le=1, description="Internet access at home: 1 for yes, 0 for no.")
