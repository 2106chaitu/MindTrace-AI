from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AnalysisHistory(Base):
    """Persisted assessment data for future history features.

    Records are created after successful predictions.
    """

    __tablename__ = "analysis_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    input_text: Mapped[str] = mapped_column(Text, nullable=False)
    predicted_label: Mapped[str] = mapped_column(String(100), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    disclaimer: Mapped[str] = mapped_column(Text, nullable=False)
    support_message: Mapped[str | None] = mapped_column(Text, nullable=True)
