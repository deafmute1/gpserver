from datetime import datetime
from secrets import compare_digest
from typing import Annotated, Union
from fastapi import Cookie, Depends, HTTPException, Request
from .database import connection, operations,models

from sqlalchemy.orm import Session

CookieHint = Annotated[Union[str, None], Cookie()] = None 

def get_db():
    db = connection.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def auth_user(username: str, sessionid: CookieHint, db: Session = Depends(get_db)): 
    token = operations.get_session(db, models.SessionToken)
    if not (
        compare_digest(token.username, username.encode('utf8')),
        compare_digest(token.key, sessionid)
    ):
        raise HTTPException(401, "Invalid Credential", {"WWW-Authenticate": "Basic"})

# Type Hint Aliases
AuthHint = Annotated[None, Depends(auth_user)]
CookieHint = Annotated[Union[str, None], Cookie()]