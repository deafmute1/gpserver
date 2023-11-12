from datetime import datetime
from secrets import compare_digest
from typing import Annotated, Union
from fastapi import Cookie, Depends, HTTPException, Request
from .database import connection, operations,models
from . import const
from sqlalchemy.orm import Session

# Type Hint Aliases
CookieHint = Annotated[Union[str, None], Cookie()]

def get_db():
    db = connection.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def auth_user(username: str, sessionid: CookieHint, db: Session = Depends(get_db)): 
    token = operations.get_session(db, models.SessionTokenTimestamp)
    if not (
        compare_digest(token.username, username.encode('utf8'))
        or compare_digest(token.key, sessionid)
    ):
        raise HTTPException(401, "Invalid Credentials", {"WWW-Authenticate": "Basic"})
    if (datetime.now() - token.created).days >= const.SESSIONID_TIMEOUT_HOURS:
        operations.delete_session(db, token)
        raise HTTPException(
            401, 
            "sessionid cookie expired; please login again", 
            {"WWW-Authenticate": "Basic"}
        )
    return username
AuthHint = Annotated[None, Depends(auth_user)]