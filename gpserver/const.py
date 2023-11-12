from enum import Enum
from os import environ
from passlib.hash import bcrypt
hasher = bcrypt()

SESSIONID_TIMEOUT_HOURS: int = int(environ.get('SESSIONID_TIMEOUT_HOURS', 120))
DATABASE_URL: str = environ.get("DATABASE_URL", "sqlite:///./database.db")

formats = Enum('formats',['json','opml','xml','text'])