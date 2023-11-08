import uvicorn
from fastapi import FastAPI
from .routers import auth

def setup_fastapi(): 
    app = FastAPI()
    app.include_router(auth.router) 

def start_server(app: FastAPI):
    config = uvicorn.Config(app)
    server = uvicorn.Server(config)
    server.run()

def main():
    start_server(setup_fastapi())

if __name__ == "__main__":
    main()