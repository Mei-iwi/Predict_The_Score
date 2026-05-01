from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    studytime: int = Field(..., ge=1, le=4, description="Mức thời gian tự học, từ 1 đến 4")
    failures: int = Field(..., ge=0, le=4, description="Số lần chưa đạt trước đó, từ 0 đến 4")
    absences: int = Field(..., ge=0, le=93, description="Số buổi vắng học, từ 0 đến 93")
    schoolsup: int = Field(..., ge=0, le=1, description="Có hỗ trợ từ nhà trường hay không")
    famsup: int = Field(..., ge=0, le=1, description="Có hỗ trợ từ gia đình hay không")
    internet: int = Field(..., ge=0, le=1, description="Có Internet tại nhà hay không")