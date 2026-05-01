from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    studytime: int = Field(..., ge=1, le=4)
    failures: int = Field(..., ge=0, le=10)
    absences: int = Field(..., ge=0, le=100)
    schoolsup: int = Field(..., ge=0, le=1)
    famsup: int = Field(..., ge=0, le=1)
    internet: int = Field(..., ge=0, le=1)