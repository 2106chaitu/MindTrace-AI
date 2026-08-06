from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "models"
DATABASE_FILE = BASE_DIR / "analysis.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE.as_posix()}"

MODEL_PATH_CANDIDATES = (
    MODEL_DIR / "model.pkl",
    MODEL_DIR / "suicide_risk_model.pkl",
)
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.pkl"
LABEL_ENCODER_PATH = MODEL_DIR / "label_encoder.pkl"

API_PREFIX = "/api/v1"
