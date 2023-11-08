from enum import Enum
from os import environ

import uvicorn
from fastapi import FastAPI
from . import database, dependencies
from .routers import auth

class Constants(Enum):
    SESSIONID_TIMEOUT_HOURS: int = int(environ.get('SESSIONID_TIMEOUT_HOURS', 120))

def setup_fastapi(): 
    app = FastAPI()
    app.add_middleware()
    app.include_router(auth.router) 

def start_server(app: FastAPI):
    config = uvicorn.Config(app)
    server = uvicorn.Server(config)
    server.run()

def main():
    start_server(setup_fastapi())

if __name__ == "__main__":
    main()