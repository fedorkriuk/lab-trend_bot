from celery import shared_task
from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Event, Trend
from ..control import pause_guard

@shared_task(name="rank_trends")
def rank_trends():
    with pause_guard("rank"):
        logger.info("Ranking trends...")
        with SessionLocal() as s:  # type: Session
            # naive: most events in last hour by entity
            rows = s.execute(
                select(Event.entity, func.count().label("cnt"))
                .group_by(Event.entity)
                .order_by(func.count().desc())
                .limit(5)
            ).all()
            for entity, cnt in rows:
                score = min(100, cnt * 10)
                t = Trend(entity=entity, score=score, rationale=f"Count={cnt}")
                s.add(t)
            s.commit()
        logger.info("Ranking done.")