from fastapi import APIRouter

from app.api.routes.assessments import router as assessments_router
from app.api.routes.health import router as health_router
from app.api.routes.history import router as history_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(assessments_router, prefix="/assessments", tags=["assessments"])
api_router.include_router(history_router, prefix="/assessments/history", tags=["history"])
