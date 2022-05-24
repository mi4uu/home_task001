import uvicorn
from fastapi import FastAPI

from .config import APP_PORT, APP_HOST
from .routes import router

app = FastAPI()


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)  # type: ignore
