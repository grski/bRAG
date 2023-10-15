from fastapi import FastAPI

from app import version
from app.chats.api import router as chat_router
from app.core.api import router as core_router
from app.core.logs import logger

# from app.core.middlewares import apply_middlewares

app = FastAPI(version=version)
# app = apply_middlewares(app)

app.include_router(core_router)
app.include_router(chat_router)

logger.info("App is ready!")
