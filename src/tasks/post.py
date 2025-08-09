from celery import shared_task
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import PostDraft
from ..control import pause_guard
from ..config import DRY_RUN, TWITTER_POSTING_ENABLED, LINKEDIN_POSTING_ENABLED

def _post_to_twitter(text: str) -> str:
    # TODO: implement POST /2/tweets with TWITTER_BEARER_TOKEN
    # return tweet id
    return "tweet:123456"

def _post_to_linkedin(text: str, links: list[str]) -> str:
    # TODO: implement POST to LinkedIn UGC or Posts API; use LINKEDIN_ACCESS_TOKEN
    # return post URN
    return "urn:li:share:123456"

@shared_task(name="publish_posts")
def publish_posts():
    with pause_guard("poster"):
        logger.info(f"Poster: DRY_RUN={DRY_RUN}")
        with SessionLocal() as s:  # type: Session
            drafts = s.execute(select(PostDraft).where(PostDraft.status == "queued")).scalars().all()
            for d in drafts:
                if DRY_RUN:
                    logger.info(f"[DRY] {d.platform.upper()} -> {d.text[:120]}")
                    d.status = "posted"
                else:
                    try:
                        if d.platform == "twitter" and TWITTER_POSTING_ENABLED:
                            rid = _post_to_twitter(d.text)
                        elif d.platform == "linkedin" and LINKEDIN_POSTING_ENABLED:
                            rid = _post_to_linkedin(d.text, d.links.split(",") if d.links else [])
                        else:
                            logger.info(f"Posting disabled for {d.platform}. Skipping.")
                            d.status = "failed"
                            continue
                        logger.info(f"Posted {d.platform}: {rid}")
                        d.status = "posted"
                    except Exception as e:
                        logger.exception(f"Post failed: {e}")
                        d.status = "failed"
                s.add(d)
            s.commit()
        logger.info("Poster: done.")