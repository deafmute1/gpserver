import base64
import secrets
from typing import Annotated, Union
from fastapi import APIRouter, Depends, Cookie, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

import time
from database import operations, models

router = APIRouter(
    prefix="/api/2/auth",
    tags=["auth"],
) 

HTTPBasicAuth = HTTPBasic()

BadResponse =JSONResponse(status_code=status.HTTP_400_BAD_REQUEST) 
NoAuthResponse =JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED) 

@router.post("/{username}/login.json")
def login(
        credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasicAuth)],
        request: Request,
        sessionid: Annotated[Union[str, None], Cookie()] = None
    ):
        if sessionid is None: 
            user: models.User = operations.get_user(credentials.username)
            if secrets.compare_digest(user.password, credentials.password):
                request.user = credentials.username
                request.session.session_cookie = "sessionid"
                request.session.secret_key = base64.b64encode(time.time()) + secrets.token_urlsafe()
            else:
                return NoAuthResponse
        elif not secrets.compare_digest(request.session.secret_key, sessionid): 
            return BadResponse

@router.post("/{username}/logout.json")
def logout(
        username: str,
        request: Request, 
        sessionid: Annotated[Union[str, None], Cookie()] = None 
    ): 
        if (not secrets.compare_digest(request.session.secret_key, sessionid) 
            or request.user != username): 
            return BadResponse 
        request.session.secret_key = None
