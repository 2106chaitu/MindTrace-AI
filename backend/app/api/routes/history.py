from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.analysis_history import AnalysisHistory
from app.schemas.history import AnalysisHistoryResponse

router = APIRouter()


@router.get("", response_model=list[AnalysisHistoryResponse])
def list_analysis_history(
    db: Session = Depends(get_db),
) -> list[AnalysisHistoryResponse]:
    """Return stored assessments with the newest analysis first."""
    statement = select(AnalysisHistory).order_by(AnalysisHistory.created_at.desc())
    return list(db.scalars(statement).all())
