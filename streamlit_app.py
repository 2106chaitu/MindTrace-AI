from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "backend" / "models"

model = joblib.load(MODEL_DIR / "suicide_risk_model.pkl")
vectorizer = joblib.load(MODEL_DIR / "tfidf_vectorizer.pkl")
label_encoder = joblib.load(MODEL_DIR / "label_encoder.pkl")