from collections.abc import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    engine = request.app.state.db_engine

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
