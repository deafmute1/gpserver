import base64
import secrets
from typing import Annotated, Optional, Union
from fastapi import APIRouter, Depends, Cookie, HTTPException, Request, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from ..const import hasher
from sqlalchemy.orm import Session

from datetime import datetime
import time 

from . import models
from ..database import operations
from .. import dependencies

router = APIRouter(
    tags=["auth"]
)

async def optional_httpbasic(request: Request):
    try: 
        return await HTTPBasic()
    except: 
        return None
    
@router.post("/{username}/login")
@router.post("/{username}/login.json")
def login(
    response: Response,
    username: str,
    credentials: Optional[HTTPBasicCredentials] = Depends(optional_httpbasic),
    db: Session = Depends(dependencies.get_db),
    sessionid: dependencies.CookieHint = None
):
    content = {'Username': username}
    with db.begin():
        if (user := operations.get_user(db, username)) is not None:
            if sessionid is not None:
                dependencies.auth_user(username,sessionid,db)
                # try: #if clients break on 401 and don't delete the cookie
                #     dependencies.auth_user(username, sessionid, db)
                # except HTTPException as err:
                #     if err.status_code == 401:
                #         response.delete_cookie("sessionid")
                #         response.status_code = 401
                #         return {'detail':err.detail}
                #     else: 
                #         raise err
                content['Authenticated'] = True
            else: # new sessionid case
                if not hasher.verify(credentials.password, user.password_hash):
                    raise HTTPException(
                        status_code=401,
                        detail="Invalid Credentials",
                        headers={"WWW-Authenticate": "Basic"}
                    )
                sessionid = secrets.token_urlsafe() 
                response.set_cookie("sessionid", sessionid)
                operations.create_session(db, models.SessionTokenTimestamp(
                    key=sessionid,
                    username=username,
                    created=datetime.now()))
                content['Authenticated'] = True
        else:
            content['Username'] = "User {username} does not exist"
    return content

@router.post("/{username}/logout")
@router.post("/{username}/logout.json")
def logout(
    response: Response,
    username: str,
    db: Session = Depends(dependencies.get_db),
    sessionid: Annotated[Union[str, None], Cookie()] = None
):
    if sessionid is None:
        raise HTTPException(400,"Not logged in")
    with db.begin():
        if (session := operations.get_session(db,models.SessionToken(key=sessionid, username=username))) is not None:
            operations.delete_session(db, session)
    response.delete_cookie("sessionid")
    return {"Username": username, "Authenticated": False}
