from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.core.templating import templates

from src.database.session import SessionDep

from src.products.service import get_all


router = APIRouter(tags=["Main Page"])


@router.get("/", response_class=HTMLResponse)
async def mainpage(request: Request, session: SessionDep):
    products = await get_all(session=session)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "Generic Retail Store",
            "products": products,
            "top_label": "All products",
            "is_index": True,
        },
    )
