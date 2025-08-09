import os
from celery import Celery
from loguru import logger
from .config import REDIS_URL
from .db import init_db

celery_app = Celery("ttb", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.timezone = "UTC"
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.accept_content = ["json"]

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Schedule cadence (tweak as needed)
    sender.add_periodic_task(60.0, ingest.s(source="github"), name="ingest_github_60s")
    sender.add_periodic_task(120.0, ingest.s(source="reddit"), name="ingest_reddit_120s")
    sender.add_periodic_task(300.0, rank_trends.s(), name="rank_trends_5m")
    sender.add_periodic_task(600.0, make_post_drafts.s(), name="editor_10m")
    sender.add_periodic_task(600.0, publish_posts.s(), name="poster_10m")

# Import tasks late to avoid circulars
from .tasks.ingest import ingest
from .tasks.rank import rank_trends
from .tasks.editor import make_post_drafts
from .tasks.post import publish_posts

# Ensure DB tables exist on worker/beat boot
init_db()
logger.info("Celery app initialized.")