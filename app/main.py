from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.utils.logging import get_logger
from config import settings

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Startup")
    yield
    logger.info("Shutdown")


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan
)


@app.get("/")
async def root():
    return {"message": settings.APP_NAME}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
