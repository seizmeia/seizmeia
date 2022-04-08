from __future__ import annotations

import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

log = logging.getLogger(__name__)

engine = create_engine(
    "sqlite:///dev.db", connect_args={"check_same_thread": False}, future=True
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = Session()
    log.debug(f"opening db session at {db.__repr__}")
    try:
        yield db
    finally:
        db.close()
        log.debug("closing db")
