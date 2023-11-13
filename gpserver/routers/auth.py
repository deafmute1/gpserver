import base64
import secrets
from typing import Annotated, Union
from fastapi import APIRouter, Depends, Cookie, HTTPException, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from const import hasher
from sqlalchemy.orm import Session

from datetime import datetime

from . import models
from ..database import operations
from .. import dependencies

router = APIRouter(
    tags=["auth"]
)

auth_scheme = HTTPBasic()


@router.post("/{username}/login.json")
def login(
    response: Response,
    username: str,
    credentials: Annotated[HTTPBasicCredentials, Depends(auth_scheme)],
    db: Session = Depends(dependencies.get_db),
    sessionid: dependencies.CookieHint = None
):
    content = {'Username': username}
    if (user := operations.get_user(db, username)) is not None:
        if sessionid is not None:
            dependencies.auth_user(username, sessionid)
            content['Authenticated'] = True
        else:
            if not hasher.verify(credentials.password, user.password_hash):
                raise HTTPException(
                    status_code=401,
                    detail="Invalid Credentials",
                    headers={"WWW-Authenticate": "Basic"}
                )
            sessionid = base64.b64encode(
                datetime.now()) + secrets.token_urlsafe()
            response.set_cookie("sessionid", sessionid)
            operations.create_session(db, models.SessionTokenTimestamp(
                key=sessionid,
                username=username,
                created=datetime.now()))
            content['Authenticated'] = True
    else:
        content['User'] = False
    return content


@router.post("/{username}/logout.json")
def logout(
    username: str,
    db: Session = Depends(dependencies.get_db),
    sessionid: Annotated[Union[str, None], Cookie()] = None
):
    if (session := operations.get_session(models.SessionToken(sessionid, username))) is None:
        raise HTTPException(400, "sessionid cookie does not authenticate user")

    operations.delete_session(db, session)
    return {"Username": username, "Authenticated": False}
