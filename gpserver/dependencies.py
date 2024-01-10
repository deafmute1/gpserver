from datetime import datetime,timedelta
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
    """
        requires db to be supplied if called directly, as Depends only runs on fastapi dep calls
    """
    if (session := operations.get_session(db,models.SessionToken(username=username,key=sessionid))) is not None:
        #check time        
        if (session.created + timedelta(hours=const.SESSIONID_TIMEOUT_HOURS)) > datetime.now():
            return username
        else:
            operations.delete_session(db,session)
    elif sessionid is not None:
        raise HTTPException(
            400,
            "sessionid provided but does not authenticate this user", 
            {"WWW-Authenticate": "Basic"}
            )
    else: 
        raise HTTPException(401, headers={"WWW-Authenticate": "Basic"})
AuthHint = Annotated[str, Depends(auth_user)]