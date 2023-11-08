from os import environ

SESSIONID_TIMEOUT_HOURS: int = int(environ.get('SESSIONID_TIMEOUT_HOURS', 120))
DATABASE_URL: str = environ.get("DATABASE_URL", "sqlite:///./database.db")