from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: Decimal = Field(
        default=None,
        max_digits=10,
        decimal_places=2,
        default=Decimal("0"),
        json_schema_extra={"examples": [19.99]},
    )
    cover: str = ""
    available: bool = Field(default=True)
    amount: int | None = Field(default=None)
    category: str = Field(default="General")
    subcategory: str | None = ""



