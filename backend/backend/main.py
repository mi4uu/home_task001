import uvicorn
from fastapi import FastAPI

from backend.config import APP_PORT, APP_HOST
from backend.routers.main_router import router as main_router
from backend.routers.files_router import router as files_router


app = FastAPI()

app.include_router(main_router)
app.include_router(files_router, prefix="/files")


if __name__ == "__main__":
    uvicorn.run("main:app", host=APP_HOST, port=int(APP_PORT), reload=True)
