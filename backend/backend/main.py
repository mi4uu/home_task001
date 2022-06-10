import uvicorn
import os
from fastapi import FastAPI
import logging
from backend.config import get_settings
from backend.routers.main_router import router as main_router
from backend.routers.files_router import router as files_router
from backend.routers.remote_api_router import router as remote_api_router

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", logging.INFO))
app = FastAPI()

app.include_router(main_router)
app.include_router(files_router, prefix="/files")
app.include_router(remote_api_router, prefix="/remote_api")


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)
