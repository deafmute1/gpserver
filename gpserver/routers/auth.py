import base64
import secrets
from typing import Annotated, Union
from fastapi import APIRouter, Depends, Cookie, HTTPException, Request 
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from datetime import datetime
from ..database import operations, models, schema
from .. import dependencies

router = APIRouter(
    prefix="/api/2/auth",
    tags=["auth"],
) 

auth_scheme = HTTPBasic()

@router.post("/{username}/login.json")
def login(
        username: str,
        credentials: Annotated[HTTPBasicCredentials, Depends(auth_scheme)],
        db: Session = Depends(dependencies.get_db),
        sessionid: dependencies.CookieHint = None
    ):
    if sessionid is None:
        # log user in 
        user: schema.User = operations.get_user(credentials.username)
        
        if not ( 
            bcrypt.verify(user.password_hash, credentials.password)
            or secrets.compare_digest(credentials.username, username)
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid Credentials", 
                headers= {"WWW-Authenticate": "Basic"}
            )
            
        operations.create_session(db, models.SessionTokenTimestamp(
            key=base64.b64encode(datetime.now()) + secrets.token_urlsafe(),
            username=user.username,
            created=datetime.now()
        ))
    else:
        # check if given cookie is valid
        session: schema.Session = operations.get_session(models.SessionToken(sessionid, username))
        if not secrets.compare_digest(sessionid, session.key):
            raise HTTPException(400, "sessionid cookie does not authenticate this user")
    return {"Username": credentials.username, "Authenticated": True}

@router.post("/{username}/logout.json")
def logout(
        username: str,
        db: Session = Depends(dependencies.get_db),       
        sessionid: Annotated[Union[str, None], Cookie()] = None 
    ): 
    session = operations.get_session(models.SessionToken(sessionid, username))
    
    if not (
        secrets.compare_digest(username, session.username)
        or secrets.compare_digest(sessionid, session.key)
    ):
        raise HTTPException(400, "sessionid cookie does not authenticate user")
    
    operations.delete_session(db, models.SessionToken(sessionid, ))
    return {"Username": username, "Authenticated": False}
