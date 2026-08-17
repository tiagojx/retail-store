from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.core.templating import templates

from src.database.session import SessionDep

from src.products.service import get_product
from src.products.service import get_product_by_category


router = APIRouter(prefix="/product", tags=["Products"])


@router.get("/{product_id}", response_class=HTMLResponse)
async def product_page(request: Request, product_id: int, session: SessionDep):
    product = await get_product(session=session, product_id=product_id)

    if not product:
        return

    return templates.TemplateResponse(
        request=request,
        name="product_page.html",
        context={
            "title": "'" + product.name + "' | GRS",
            "product": product,
        },
    )


@router.get("/c/{category}/{subcategory}")
@router.get("/c/{category}")
async def product_by_category(
    request: Request, session: SessionDep, category: str, subcategory: str | None = None
):
    products = await get_product_by_category(session, category, subcategory)

    title = subcategory if subcategory else category
    top_label = subcategory if subcategory else category

    return templates.TemplateResponse(
        request=request,
        name="search_results.html",
        context={
            "title": title + " are in GRS!",
            "top_label": top_label,
            "search_results": products,
        },
    )
