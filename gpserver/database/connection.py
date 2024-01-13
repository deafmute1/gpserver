from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .schema import Base
from .. import const

engine = create_engine(
    const.DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)