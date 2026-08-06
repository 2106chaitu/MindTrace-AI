from app.db.base import Base
from app.db.session import engine
# Import ORM modules before metadata creation so their tables are registered.
from app.models.analysis_history import AnalysisHistory  # noqa: F401


def initialize_database() -> None:
    """Create required tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)
