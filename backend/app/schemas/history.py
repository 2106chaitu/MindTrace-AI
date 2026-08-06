from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnalysisHistoryResponse(BaseModel):
    """Read-only API representation of a stored assessment."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    input_text: str
    predicted_label: str
    risk_level: str
    confidence: float
    disclaimer: str
    support_message: str | None
