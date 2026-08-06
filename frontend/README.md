# React frontend

## Start locally

```powershell
cd frontend
npm install
npm run dev
```

The development server runs at `http://127.0.0.1:5173`. Its `/api/v1/assessments` request is proxied to the FastAPI endpoint at `http://127.0.0.1:8000/api/v1/assessments`.

To target a deployed backend, create `.env` with:

```text
VITE_API_URL=https://your-api.example.com/api/v1
```
