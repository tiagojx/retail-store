from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.commons.button import Button
from backend.internal.database.db import DB
from backend.internal.database.sql import SQL
from backend.internal.product import product


load_dotenv()

db = DB()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")

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
    results = await product.get_all_items(db.conn)

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
    results = await product.select_item(query, db.conn)

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


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    no_header = True
    buttons = [
        Button(id=1, label="New", redirect_to="dashboard/product/new"),
        Button(id=2, label="Edit", redirect_to="dashboard/product/edit"),
        Button(id=3, label="Delete", redirect_to="dashboard/product/edit?delete=on"),
    ]

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "title": "Dashboard | GMS Management System",
            "no_header": no_header,
            "buttons": buttons,
        },
    )


@app.get("/dashboard/product/new", response_class=HTMLResponse)
async def d_new_product(request: Request):
    no_header = True

    return templates.TemplateResponse(
        request=request,
        name="dashboard_new_product.html",
        context={"title": "New -Product- | GMS Dashboard", "no_header": no_header},
    )


@app.get("/dashboard/product/edit")
async def d_edit_product(delete: bool = False):
    return f"Pretend there's something here. Delete mode: {delete}"


@app.post("/redirect")
async def redirect_handler(target: str = Form(...)):
    return RedirectResponse(url=target, status_code=status.HTTP_303_SEE_OTHER)
