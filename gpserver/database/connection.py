from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from ..main import Constants

engine = create_engine(
    Constants.DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)