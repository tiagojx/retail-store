from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from typing import Annotated, Optional
from fastapi import FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.commons.button import Button
from backend.internal.database.db import DB
from backend.internal.models import product


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


async def alphabetical_sorting(og_list) -> list:
    filtered = []

    index = []
    for item in og_list:
        index.append(item.name)

    sorted_index = sorted(index, key=str.lower)

    for n in sorted_index:
        for item in og_list:
            if item.name == n:
                filtered.append(item)

    return filtered


@app.get("/", response_class=HTMLResponse)
async def mainpage(request: Request, name: str = "Guest"):
    results = await product.get_all_items(db.conn)

    filtered = await alphabetical_sorting(results)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "Generic Merch Store",
            "name": name,
            "results": filtered,
            "top_label": "All products",
            "is_index": True,
        },
    )


@app.get("/product/{p_id}", response_class=HTMLResponse)
async def product_page(request: Request, p_id: int):
    prod = await product.get_item_by_id(p_id, db.conn)

    return templates.TemplateResponse(
        request=request,
        name="product_page.html",
        context={
            "title": "'" + prod.name + "' | GMS",
            "product": prod,
        },
    )


@app.get("/product/c/{category}/{subcategory}")
@app.get("/product/c/{category}", response_class=HTMLResponse)
async def product_by_category(
    request: Request, category: str, subcategory: Optional[str] = None
):
    results = await product.get_item_by_category(category, subcategory, db.conn)

    filtered = await alphabetical_sorting(results)

    title = subcategory if subcategory else category
    top_label = subcategory if subcategory else category

    return templates.TemplateResponse(
        request=request,
        name="search_results.html",
        context={
            "title": title + " are in GMS!",
            "results": filtered,
            "top_label": top_label,
        },
    )


@app.get("/search", response_class=HTMLResponse)
async def search_get(request: Request, query: str):
    results = await product.select_item(query, db.conn)

    filtered = await alphabetical_sorting(results)

    return templates.TemplateResponse(
        request=request,
        name="search_results.html",
        context={
            "title": "The best '" + query + "' for you | GMS",
            "search_query": query,
            "results": filtered,
            "top_label": "Search: " + query,
        },
    )


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
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
            "no_header": True,
            "buttons": buttons,
        },
    )


@app.get("/dashboard/product/new", response_class=HTMLResponse)
async def d_new_prod(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard_new_product.html",
        context={
            "title": "New - Product | GMS Dashboard",
            "no_header": True,
            "redirect_to": "/dashboard#product",
        },
    )


@app.post("/dashboard/product/new", response_class=HTMLResponse)
async def submit_new_prod(
    request: Request, data: Annotated[product.NewProdForm, Form()]
):
    results = await product.new_product(data, db.conn)
    if results.status_code == 500:
        raise HTTPException(status_code=500, detail=results.message)

    results_message = results.message + ": '" + data.name + "'"
    return templates.TemplateResponse(
        request=request,
        name="dashboard_new_product.html",
        context={
            "title": "New - Product | GMS Dashboard",
            "no_header": True,
            "redirect_to": "/dashboard#product",
            "results_message": results_message,
        },
    )


@app.get("/dashboard/product/edit")
async def d_edit_product(delete: bool = False):
    return f"Pretend there's something here. Delete mode: {delete}"


@app.post("/redirect")
async def redirect_handler(target: str = Form(...)):
    return RedirectResponse(url=target, status_code=status.HTTP_303_SEE_OTHER)
