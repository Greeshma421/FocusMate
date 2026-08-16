FocusMate API (Phase 1)

Setup (Windows PowerShell):
1. From repo root: cd apps\api
2. Create virtualenv: python -m venv .venv
3. Activate: .\.venv\Scripts\Activate.ps1
4. Install dependencies: pip install -r requirements.txt
5. Copy environment variables: copy ..\.env.example .env  (edit .env as needed)
6. Start Postgres with Docker Compose from repo root: docker compose up -d
7. Run server: uvicorn app.main:app --reload --port 8000

API endpoints:
- GET /api/v1/health
- POST /api/v1/auth/register
- POST /api/v1/auth/login

