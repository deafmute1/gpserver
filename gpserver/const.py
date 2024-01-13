#from importlib import metadata
from os import environ
from typing import Literal
from passlib.hash import bcrypt

# Exposed Constants 
SESSIONID_TIMEOUT_HOURS: int = int(environ.get('SESSIONID_TIMEOUT_HOURS', 120))
DATABASE_URL: str = environ.get("DATABASE_URL", "sqlite:///./database.db")

# Internal
hasher = bcrypt
#version = metadata.version("gpserver")
formats = ['json','opml','xml','text']
formatsLiteral = Literal['json','opml','xml','text']
actions = ["download", "play", "delete", "new"]
episodeActionsLiteral = Literal["download", "play", "delete", "new"]