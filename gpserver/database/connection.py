from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# TODO change this to be at project root when dockerising
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()