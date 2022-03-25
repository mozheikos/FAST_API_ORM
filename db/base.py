from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from core.config import DATABASE_URL


def get_engine():
    return create_engine(DATABASE_URL)


def get_session():
    return Session(bind=get_engine())


Base = declarative_base()
