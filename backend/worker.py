import os
from celery import Celery
from database import SessionLocal
import swarm_engine

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "swarm_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

def execute_swarm_task(run_id: int):
    db = SessionLocal()
    try:
        swarm_engine.run_swarm_pipeline(run_id, db)
    finally:
        db.close()

@celery_app.task(name="worker.run_swarm_task")
def run_swarm_task(run_id: int):
    execute_swarm_task(run_id)
