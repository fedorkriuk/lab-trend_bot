import os
import time
from contextlib import contextmanager
from sqlalchemy import select
from sqlalchemy.orm import Session
from loguru import logger
from .config import KILL_SWITCH_PATH
from .db import SessionLocal
from .models import SystemState

def get_state(session: Session) -> SystemState:
    state = session.execute(select(SystemState).where(SystemState.id == 1)).scalar_one_or_none()
    if not state:
        state = SystemState(id=1, paused=False)
        session.add(state)
        session.commit()
        session.refresh(state)
    return state

def set_paused(paused: bool, reason: str | None = None):
    with SessionLocal() as s:
        st = get_state(s)
        st.paused = paused
        st.reason = reason
        s.commit()
        logger.warning(f"System paused={paused}. Reason={reason}")

def is_paused() -> bool:
    if os.path.exists(KILL_SWITCH_PATH):
        return True
    with SessionLocal() as s:
        return get_state(s).paused

def wait_if_paused(poll_sec: int = 5):
    while is_paused():
        logger.info("Paused. Sleeping...")
        time.sleep(poll_sec)

@contextmanager
def pause_guard(task_name: str):
    # Call at task start; yields only when unpaused
    wait_if_paused()
    try:
        yield
    finally:
        # if paused during execution, next task will block
        return