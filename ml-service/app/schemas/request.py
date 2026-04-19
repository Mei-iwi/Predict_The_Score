from pydantic import BaseModel

class PredictionRequest(BaseModel):
    studytime: int
    failures: int
    absences: int
    schoolsup: int
    famsup: int
    internet: int