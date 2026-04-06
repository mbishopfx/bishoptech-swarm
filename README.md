# BishopTech Swarm

A multi-agent sequential swarm orchestration system built for high-agency processing across xAI and Gemini APIs.

## Architecture
- **Backend**: Python (FastAPI + Celery + Redis + PostgreSQL)
- **Frontend**: Next.js 14 (App Router, Tailwind CSS)
- **CLI**: Python Typer

## Getting Started Locally

### Backend & Worker
1. `cd backend`
2. Create `venv` and `pip install -r requirements.txt`
3. Run Redis locally (`docker run -p 6379:6379 -d redis`)
4. Set `.env` variables: `XAI_API_KEY`, `GEMINI_API_KEY`
5. Start FastAPI: `uvicorn main:app --reload`
6. Start Celery worker: `celery -A worker.celery_app worker --loglevel=info`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

### CLI
1. `cd cli`
2. `pip install -r requirements.txt`
3. Try it: `python main.py --help`

## Deployment
- **Railway**: Deploy the `backend/` directory, provision Postgres and Redis. Create two services: one for `uvicorn main:app --host 0.0.0.0 --port $PORT` and one for the Celery worker.
- **Vercel**: Deploy the `frontend/` directory pointing to the Railway API URL.
