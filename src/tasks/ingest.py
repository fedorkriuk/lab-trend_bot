from celery import shared_task
from loguru import logger
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Event
from ..control import pause_guard

@shared_task(name="ingest")
def ingest(source: str = "github"):
    with pause_guard("ingest"):
        logger.info(f"Ingest start: {source}")
        # TODO: Replace with real API pulls; below is a stub event
        stub = {"entity": "cool-repo/cool-lib", "url": "https://github.com/cool-repo/cool-lib"}
        with SessionLocal() as s:  # type: Session
            ev = Event(source=source, entity=stub["entity"], payload=str(stub))
            s.add(ev); s.commit()
        logger.info(f"Ingest done: {source}")