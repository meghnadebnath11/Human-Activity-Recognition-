from typing import List

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    acc_x: float = Field(..., description="Accelerometer X-axis reading")
    acc_y: float = Field(..., description="Accelerometer Y-axis reading")
    acc_z: float = Field(..., description="Accelerometer Z-axis reading")
    gyro_x: float = Field(..., description="Gyroscope X-axis reading")
    gyro_y: float = Field(..., description="Gyroscope Y-axis reading")
    gyro_z: float = Field(..., description="Gyroscope Z-axis reading")


class PredictionResponse(BaseModel):
    predicted_activity: str
    class_probabilities: dict[str, float]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


class ProjectMetadataResponse(BaseModel):
    model_loaded: bool
    classes: List[str]
    accuracy: float
    macro_f1: float
    feature_columns: List[str]
