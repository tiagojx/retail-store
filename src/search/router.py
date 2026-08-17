from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from src.core.templating import templates

from src.database.session import SessionDep

from src.products.service import product_search


router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/", response_class=HTMLResponse)
async def search_get(request: Request, session: SessionDep, query: str):
    search_results = await product_search(session, query)

    return templates.TemplateResponse(
        request=request,
        name="search_results.html",
        context={
            "title": "The Best '" + query + "' for you | GRS",
            "search_query": query,
            "search_results": search_results,
            "top_label": "Search: " + query,
        },
    )


@router.post("/", response_class=HTMLResponse)
async def search_post(
    request: Request, session: SessionDep, query: Annotated[str, Form()] = ""
):
    search_results = []

    if query.strip():
        search_results = await product_search(session, query)

    return templates.TemplateResponse(
        request=request,
        name="layouts/partials/search_preview_row.html",
        context={
            "products": search_results,
        },
    )
