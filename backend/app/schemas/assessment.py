from pydantic import BaseModel, Field


class AssessmentRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10_000, description="Text to assess")


class AssessmentResponse(BaseModel):
    label: str
    risk_level: str
    confidence: float = Field(..., ge=0, le=100)
    disclaimer: str
    support_message: str | None = None
