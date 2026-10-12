from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


class Settings(BaseSettings):
    database_url: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    engine: AsyncEngine = create_async_engine(
        settings.database_url,
        pool_pre_ping=True,
    )
    app.state.db_engine = engine

    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(
    title="WareX API",
    description="Warehouse Management Platform",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", tags=["System"])
async def root():
    return {"name": "WareX API", "version": "0.1.0", "status": "running"}


@app.get("/health/live", tags=["Health"])
async def liveness():
    return {"status": "alive"}


@app.get("/health/ready", tags=["Health"])
async def readiness():
    engine: AsyncEngine = app.state.db_engine

    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(status_code=503, detail="Database is not ready")

    return {"status": "ready", "database": "connected"}
