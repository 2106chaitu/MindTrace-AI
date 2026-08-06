from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.assessment import AssessmentRequest, AssessmentResponse
from app.services.history_service import save_prediction_history_safely
from app.services.model_service import assessment_service, predict_text

router = APIRouter()


@router.post("", response_model=AssessmentResponse, status_code=status.HTTP_200_OK)
def assess_text(
    payload: AssessmentRequest, db: Session = Depends(get_db)
) -> AssessmentResponse:
    """Classify submitted text using the trained model."""
    if not assessment_service.is_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Assessment model is unavailable.",
        )

    try:
        prediction = predict_text(payload.text)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    save_prediction_history_safely(db, input_text=payload.text, prediction=prediction)
    return prediction
