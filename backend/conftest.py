import pytest
from httpx import ASGITransport, AsyncClient
from main import app, lifespan
from src.database import Base, engine, SessionLocal

@pytest.fixture(scope="function", autouse=True)
async def session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with SessionLocal() as session:
        try:
            yield session 
        finally:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="function")
async def client():
    async with lifespan(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="sqlite+aiosqlite://"
        ) as client:
            yield client