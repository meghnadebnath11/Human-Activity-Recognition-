from __future__ import annotations

import json
import logging
from pathlib import Path

import joblib

from backend.app.core.config import get_settings
from backend.app.models.schemas import PredictionRequest
from ml.src.features import engineer_single_prediction_features

LOGGER = logging.getLogger(__name__)


class ModelNotReadyError(RuntimeError):
    pass


class InferenceService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.metrics = {
            "classes": [],
            "accuracy": 0.0,
            "macro_f1": 0.0,
            "feature_columns": [],
        }
        self._load_artifacts()

    @property
    def is_ready(self) -> bool:
        return self.model is not None and self.scaler is not None and self.label_encoder is not None

    def _resolve_path(self, relative_path: str) -> Path:
        project_root = Path(__file__).resolve().parents[3]
        return project_root / relative_path

    def _load_artifacts(self) -> None:
        model_path = self._resolve_path(self.settings.model_path)
        scaler_path = self._resolve_path(self.settings.scaler_path)
        label_encoder_path = self._resolve_path(self.settings.label_encoder_path)
        metrics_path = self._resolve_path(self.settings.metrics_path)

        if not all(path.exists() for path in [model_path, scaler_path, label_encoder_path, metrics_path]):
            LOGGER.warning("Model artifacts are not available yet. Run the training pipeline before serving predictions.")
            return

        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.label_encoder = joblib.load(label_encoder_path)
        with metrics_path.open("r", encoding="utf-8") as file_handle:
            self.metrics = json.load(file_handle)
        LOGGER.info("ML artifacts loaded successfully.")

    def get_metadata(self) -> dict:
        return {
            "model_loaded": self.is_ready,
            **self.metrics,
        }

    def predict(self, payload: PredictionRequest) -> dict:
        if not self.is_ready:
            raise ModelNotReadyError("Model artifacts are missing. Train the model before calling /predict.")

        sample = engineer_single_prediction_features(payload.model_dump())
        transformed = self.scaler.transform(sample)
        probabilities = self.model.predict_proba(transformed)[0]
        predicted_index = int(probabilities.argmax())
        predicted_activity = self.label_encoder.inverse_transform([predicted_index])[0]

        class_probabilities = {
            label: round(float(probability), 4)
            for label, probability in zip(self.label_encoder.classes_, probabilities, strict=True)
        }

        return {
            "predicted_activity": predicted_activity,
            "class_probabilities": class_probabilities,
        }
