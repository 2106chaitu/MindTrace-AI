from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import API_PREFIX
from app.db.init_db import initialize_database
from app.services.model_service import assessment_service


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    assessment_service.load()
    yield


app = FastAPI(
    title="Suicide Risk Assessment API",
    version="1.0.0",
    description="Educational text-screening API; it does not provide a clinical diagnosis.",
    lifespan=lifespan,
)
app.include_router(api_router, prefix=API_PREFIX)
