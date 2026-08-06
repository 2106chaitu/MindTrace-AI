import re
import string
from typing import Any

import joblib
import numpy as np

from app.core.config import (
    LABEL_ENCODER_PATH,
    MODEL_PATH_CANDIDATES,
    VECTORIZER_PATH,
)
from app.schemas.assessment import AssessmentResponse


DISCLAIMER = (
    "This automated screening result is not a medical diagnosis or a substitute for professional care."
)

SUPPORT_MESSAGE = (
    "If there is immediate danger, contact local emergency services. "
    "Consider reaching out to a trusted person or a qualified mental-health professional."
)


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


class AssessmentService:
    def __init__(self) -> None:
        self.model: Any | None = None
        self.vectorizer: Any | None = None
        self.label_encoder: Any | None = None

    @property
    def is_ready(self) -> bool:
        return (
            self.model is not None
            and self.vectorizer is not None
            and self.label_encoder is not None
        )

    def load(self) -> None:
        model_path = next(
            (path for path in MODEL_PATH_CANDIDATES if path.is_file()),
            None,
        )

        if model_path is None:
            expected = ", ".join(path.name for path in MODEL_PATH_CANDIDATES)
            raise FileNotFoundError(
                f"Model file not found. Expected one of: {expected}"
            )

        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(VECTORIZER_PATH)
        self.label_encoder = joblib.load(LABEL_ENCODER_PATH)

        print("=" * 60)
        print("Loaded Model Path :", model_path)
        print("Loaded Model Type :", type(self.model))
        print("Label Classes     :", self.label_encoder.classes_)
        print("=" * 60)

    def assess(self, text: str) -> AssessmentResponse:
        cleaned = clean_text(text)

        if not cleaned:
            raise ValueError(
                "Text must include at least one non-punctuation character."
            )

        transformed = self.vectorizer.transform([cleaned])

        prediction = self.model.predict(transformed)[0]
        label = self.label_encoder.inverse_transform([prediction])[0]

        # Decision score from Logistic Regression
        score = float(self.model.decision_function(transformed)[0])

        # Convert score to probability/confidence
        confidence = round(
            1 / (1 + np.exp(-abs(score))) * 100,
            2,
        )

        elevated = label.lower() == "suicide"

        return AssessmentResponse(
            label=label,
            risk_level="elevated" if elevated else "low",
            confidence=confidence,
            disclaimer=DISCLAIMER,
            support_message=SUPPORT_MESSAGE if elevated else None,
        )


assessment_service = AssessmentService()


def predict_text(text: str) -> AssessmentResponse:
    if not assessment_service.is_ready:
        raise RuntimeError("Assessment model is unavailable.")

    return assessment_service.assess(text)