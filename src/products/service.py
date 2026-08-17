from decimal import Decimal

from typing import Annotated

from fastapi import Form

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.products.models import Product
from src.products.schemas import ProductSchema


# GET services


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def get_all(session: AsyncSession):
    results = await session.exec(select(Product))
    return results.all()


async def product_search(session: AsyncSession, query: str):
    results = await session.exec(select(Product).where(Product.name.contains(query)))
    return results.all()


async def get_product_by_category(
    session: AsyncSession, category: str, subcategory: str | None = None
):
    if subcategory:
        results = await session.exec(
            select(Product).where(Product.subcategory == subcategory)
        )
        return results.all()

    results = await session.exec(select(Product).where(Product.category == category))
    return results.all()


# POST services


async def new_product(
    session: AsyncSession, data: Annotated[ProductSchema, Form()]
) -> tuple[str, int]:
    # (message_str, return_int)
    message = ()

    try:
        product = Product(
            name=data.name,
            price=Decimal(data.price),
            cover=data.cover,
            amount=int(data.amount),
            category=data.category,
            subcategory=data.subcategory if data.subcategory else None,
            available=True,
        )

        session.add(product)
    except Exception as e:
        message = (f"error: {e}", 1)
    else:
        await session.commit()
        await session.refresh(product)
        message = (f"{data.name} added to database with ID = {product.id}.", 0)

    return message
