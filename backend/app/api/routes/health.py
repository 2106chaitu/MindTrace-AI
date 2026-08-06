from fastapi import APIRouter

from app.services.model_service import assessment_service

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    """Return service readiness without exposing model internals."""
    return {"status": "ok" if assessment_service.is_ready else "degraded"}
