import logging

from sqlalchemy.orm import Session

from app.models.analysis_history import AnalysisHistory
from app.schemas.assessment import AssessmentResponse

logger = logging.getLogger(__name__)


def save_prediction_history(
    db: Session, *, input_text: str, prediction: AssessmentResponse
) -> None:
    """Persist one completed assessment in the current database session.

    The caller owns error handling so persistence failures cannot affect the
    assessment response delivered to the API client.
    """
    record = AnalysisHistory(
        input_text=input_text,
        predicted_label=prediction.label,
        risk_level=prediction.risk_level,
        confidence=prediction.confidence,
        disclaimer=prediction.disclaimer,
        support_message=prediction.support_message,
    )
    db.add(record)
    db.commit()


def save_prediction_history_safely(
    db: Session, *, input_text: str, prediction: AssessmentResponse
) -> None:
    """Persist an assessment without allowing database failures to break inference."""
    try:
        save_prediction_history(db, input_text=input_text, prediction=prediction)
    except Exception:
        try:
            db.rollback()
        except Exception:
            logger.exception("Unable to roll back failed assessment-history transaction")
        logger.exception("Unable to save assessment history; returning prediction normally")
