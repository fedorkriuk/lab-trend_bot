import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "local")
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "TrendBot/0.1")

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_POSTING_ENABLED = os.getenv("TWITTER_POSTING_ENABLED", "false").lower() == "true"

LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_ORG_URN = os.getenv("LINKEDIN_ORG_URN")  # e.g., "urn:li:organization:XXXX"
LINKEDIN_POSTING_ENABLED = os.getenv("LINKEDIN_POSTING_ENABLED", "false").lower() == "true"

KILL_SWITCH_PATH = os.getenv("KILL_SWITCH_PATH", "/app/.paused")