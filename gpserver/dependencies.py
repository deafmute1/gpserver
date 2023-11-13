from datetime import datetime
from typing import Annotated, Union
from fastapi import Cookie, Depends, HTTPException

from .routers import models
from .database import connection, operations
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
    if (session := operations.get_session(db,models.SessionToken(username=username,key=sessionid))) is not None:
        #check time
        if (datetime.now() - session.created) < const.SESSIONID_TIMEOUT_HOURS:
            return username
        else:
            operations.delete_session(db,session)
    raise HTTPException(
        401,
        "sessionid does not authenticate this user; please login again", 
        {"WWW-Authenticate": "Basic"}
        )
AuthHint = Annotated[str, Depends(auth_user)]