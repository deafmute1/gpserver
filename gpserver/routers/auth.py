import base64
import secrets
from typing import Annotated, Union
from fastapi import APIRouter, Depends, Cookie, HTTPException, Request, 
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.hash import bcrypt

import time
from ..database import operations, models, schema
from .. import dependencies
from ..dependencies import StatusResponses

router = APIRouter(
    prefix="/api/2/auth",
    tags=["auth"],
) 

HTTPBasicAuth = HTTPBasic()

@router.post("/{username}/login.json")
def login(
        credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasicAuth)],
        request: Request,
        sessionid: Annotated[Union[str, None], Cookie()] = None
    ):
        if sessionid is None: 
            user: schema.User = operations.get_user(credentials.username)
            if bcrypt.verify(user.password_hash, credentials.password):
                request.user = credentials.username
                request.session['session_cookie'] = "sessionid"
                request.session['secret_key'] = base64.b64encode(time.time()) + secrets.token_urlsafe()
            else:
                raise HTTPException(401,"Invalid Credentials") 
        elif not secrets.compare_digest(request.session['secret_key'], sessionid): 
            raise HTTPException(400, "sessionid cookie does not authneticate this user")
        return

@router.post("/{username}/logout.json")
def logout(
        username: str,
        request: Request, 
        sessionid: Annotated[Union[str, None], Cookie()] = None 
    ): 
        if (not secrets.compare_digest(request.session.secret_key, sessionid) 
            or request.user != username): 
            raise HTTPException(400, "sessionid cookie does not match user")
        request.session.secret_key = None
