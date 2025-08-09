from fastapi import FastAPI
from pydantic import BaseModel
from .db import init_db
from .control import set_paused, is_paused
from .config import DRY_RUN
from loguru import logger

app = FastAPI(title="Tech Trend Bot")

class PauseRequest(BaseModel):
    paused: bool
    reason: str | None = None

@app.on_event("startup")
def startup_event():
    init_db()
    logger.info("API started. DRY_RUN=%s", DRY_RUN)

@app.get("/health")
def health():
    return {"status": "ok", "paused": is_paused(), "dry_run": DRY_RUN}

@app.post("/control/pause")
def pause(req: PauseRequest):
    set_paused(req.paused, req.reason)
    return {"paused": req.paused, "reason": req.reason}

@app.get("/control/status")
def status():
    return {"paused": is_paused(), "dry_run": DRY_RUN}