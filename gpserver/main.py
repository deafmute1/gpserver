import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from . import dependencies, routers, db

def setup_fastapi(): 
    app = FastAPI()
    app.add(SessionMiddleware)
    app.include_router(routers.auth) 

def start_server(app: FastAPI):
    config = uvicorn.Config(app)
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    start_server(setup_fastapi())