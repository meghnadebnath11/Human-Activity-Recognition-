from fastapi import APIRouter, HTTPException, status

from ..models.schemas import HealthResponse, PredictionRequest, PredictionResponse, ProjectMetadataResponse
from ..services.inference import InferenceService, ModelNotReadyError

api_router = APIRouter()
inference_service = InferenceService()


@api_router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", model_loaded=inference_service.is_ready)


@api_router.get("/metadata", response_model=ProjectMetadataResponse)
def project_metadata() -> ProjectMetadataResponse:
    metadata = inference_service.get_metadata()
    return ProjectMetadataResponse(**metadata)


@api_router.post("/predict", response_model=PredictionResponse, status_code=status.HTTP_200_OK)
def predict_activity(payload: PredictionRequest) -> PredictionResponse:
    try:
        prediction = inference_service.predict(payload)
        return PredictionResponse(**prediction)
    except ModelNotReadyError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

