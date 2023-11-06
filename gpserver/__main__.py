import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}

def main():
    config = uvicorn.Config(app)
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    main()