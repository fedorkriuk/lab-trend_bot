from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, Text, TIMESTAMP, func
from .db import Base

class SystemState(Base):
    __tablename__ = "system_state"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    paused: Mapped[bool] = mapped_column(Boolean, default=False)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)

class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(32))   # github|reddit|x
    entity: Mapped[str] = mapped_column(String(256))  # repo/package/topic
    payload: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

class Trend(Base):
    __tablename__ = "trends"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity: Mapped[str] = mapped_column(String(256), index=True)
    score: Mapped[int] = mapped_column(Integer)       # 0..100
    rationale: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

class PostDraft(Base):
    __tablename__ = "post_drafts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    platform: Mapped[str] = mapped_column(String(16))  # twitter|linkedin
    text: Mapped[str] = mapped_column(Text)
    links: Mapped[str] = mapped_column(Text)           # csv or json
    status: Mapped[str] = mapped_column(String(16), default="queued")  # queued|posted|failed
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())