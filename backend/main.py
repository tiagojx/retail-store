from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.internal.database.db import DB
from backend.internal.database.sql import SQL
from backend.internal.handler import item_handler


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")
    db = DB()

    try:
        conn_fmt = {"user": os.getenv("DB_USER"), "password": os.getenv("DB_PASSWD")}

        conn_str = "postgresql://{user}:{password}@localhost:5432/main".format(
            **conn_fmt
        )
        db.new_connection(conn_str)
    except Exception as e:
        print(f"An error ocurred: {e}")
        if db.conn:
            db.conn.rollback()

    yield

    db.disconnect()


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def mainpage(request: Request, name: str = "Guest"):
    results = await item_handler.get_all_items()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "Generic Merch Store",
            "name": name,
            "results": results,
            "top_label": "All products",
        },
    )


@app.get("/search", response_class=HTMLResponse)
async def search_box(request: Request, query: str):
    results = await item_handler.select_item(query)

    return templates.TemplateResponse(
        request=request,
        name="search_results.html",
        context={
            "title": "The best '" + query + "' for you | GMS",
            "search_query": query,
            "results": results,
            "top_label": "Search: " + query,
        },
    )
