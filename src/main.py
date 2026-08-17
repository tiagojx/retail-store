from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from sqlmodel import SQLModel

from src.database.session import engine

# Importing routers
from src.index.router import router as index_router
from src.products.router import router as products_router
from src.search.router import router as search_router
from src.dashboard.router import router as dashboard_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting...")

    # await asyncio.to_thread(SQLModel.metadata.create_all, engine)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Database tables created successfully.")

    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(index_router)
app.include_router(products_router)
app.include_router(search_router)
app.include_router(dashboard_router)
