from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from src.core.templating import templates

from src.database.session import SessionDep

from src.products.schemas import ProductSchema
from src.products.service import new_product

from src.models import Button


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# GET requests
@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    buttons = [
        Button(id=1, label="New", redirect_to="product/new"),
        Button(id=2, label="Edit", redirect_to="product/edit"),
        Button(id=3, label="Delete", redirect_to="product/edit?delete=on"),
    ]

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "title": "Dashboard | GRS ADMIN",
            "buttons": buttons,
            "no_header": True,
        },
    )


@router.get("/product/new", response_class=HTMLResponse)
async def add_product_get(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard_add_product.html",
        context={
            "title": "Add Product | GRS ADMIN",
            "redirect_to": "/dashboard#product",
            "no_header": True,
        },
    )


# POST requests
@router.post("/product/new", response_class=HTMLResponse)
async def add_product_post(
    request: Request,
    session: SessionDep,
    product_data: Annotated[ProductSchema, Form()],
):
    message = await new_product(session=session, data=product_data)

    return templates.TemplateResponse(
        request=request,
        name="layouts/partials/dashboard_log.html",
        context={
            "message_log": message,
        },
    )
