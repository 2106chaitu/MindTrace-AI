# Suicide Risk Assessment API

FastAPI backend for the existing trained classifier. Model artifacts stay in `models/` and are loaded once when the service starts. The loader accepts `model.pkl` or the included `suicide_risk_model.pkl` classifier artifact.

## Layout

```text
app/
  api/routes/       # HTTP endpoints
  core/             # configuration
  schemas/          # API contracts
  services/         # model inference and text normalization
models/             # trained model artifacts
analysis.db          # SQLite database, created at startup
```

## Database

The backend initializes `analysis.db` at startup with an `analysis_history` table. Each successful prediction is saved after inference. If persistence fails, the API still returns the generated prediction normally.

## Run

```powershell
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation.

## Endpoints

- `GET /api/v1/health`
- `POST /api/v1/assessments`
- `GET /api/v1/assessments/history`

Example request body:

```json
{ "text": "I feel overwhelmed and hopeless." }
```

Example response:

```json
{
  "label": "suicide",
  "risk_level": "elevated",
  "confidence": 91.42,
  "disclaimer": "This automated screening result is not a medical diagnosis or a substitute for professional care.",
  "support_message": "If there is immediate danger, contact local emergency services. Consider reaching out to a trusted person or a qualified mental-health professional."
}
```

This API is for educational screening only. It is not a crisis service or a clinical diagnostic tool.

## Python usage

After application startup has loaded the artifacts, inference is also available as a reusable function:

```python
from app.services.model_service import predict_text

result = predict_text("I feel overwhelmed and hopeless.")
```
