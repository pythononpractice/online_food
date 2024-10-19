from collections import defaultdict
import uvicorn
from fastapi import FastAPI
from app.api.routers import main_router

from app.core.config import settings

app = FastAPI(root_path=settings.API_ROOT_PATH, title=settings.APP_TITLE)

app.include_router(main_router)


if __name__ == "main":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
