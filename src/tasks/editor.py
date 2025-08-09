from celery import shared_task
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Trend, PostDraft
from ..control import pause_guard
from ..util.llm import summarize_to_post

@shared_task(name="make_post_drafts")
def make_post_drafts():
    with pause_guard("editor"):
        logger.info("Editor: creating post drafts...")
        with SessionLocal() as s:  # type: Session
            top = s.execute(select(Trend).order_by(Trend.score.desc()).limit(3)).scalars().all()
            for tr in top:
                evidence = [{"title": "Repo", "url": "https://example.com"}]
                for platform in ["twitter", "linkedin"]:
                    pd = summarize_to_post({"entity": tr.entity, "score": tr.score, "evidence": evidence}, platform)
                    draft = PostDraft(platform=platform, text=pd["text"], links=",".join(pd["links"]))
                    s.add(draft)
            s.commit()
        logger.info("Editor: drafts created.")