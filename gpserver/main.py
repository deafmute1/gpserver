import uvicorn
from fastapi import FastAPI
from .routers import auth,admin,subscriptions,device,alive



def setup_fastapi(): 
    app = FastAPI()
    app.include_router(auth.router,prefix="/api/2/auth") 
    app.include_router(admin.router,prefix="/api/admin")
    #app.include_router(subscriptions.router_v1,prefix="/subscriptions") 
    app.include_router(subscriptions.router_v2,prefix="/api/2/subscriptions")
    app.include_router(device.devices_router,prefix="/api/2/devices")
    app.include_router(device.devices_updates_router,prefix="/api/2/updates")
    app.include_router(alive.router)
    
    return app

def start_server(app: FastAPI):
    config = uvicorn.Config(app)
    server = uvicorn.Server(config)
    server.run()

def main():
    start_server(setup_fastapi())

if __name__ == "__main__":
    main()