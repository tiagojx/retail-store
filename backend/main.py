from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .internal.database import db

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def mainpage(request: Request, name: str = "Guest"):
    results = await db.get_all_items()

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
    results = await db.select_item(query)

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
