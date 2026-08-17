from decimal import Decimal

from sqlmodel import Column, Numeric, SQLModel, Field


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: Decimal = Field(
        default=Decimal("0"),
        max_digits=10,
        decimal_places=2,
        sa_column=Column(
            Numeric(precision=10, scale=2), nullable=False, server_default="0"
        ),
        schema_extra={"examples": [19.99]},
    )
    cover: str = ""
    available: bool = Field(default=True)
    amount: int | None = Field(default=None)
    category: str = Field(default="General", nullable=False)
    subcategory: str | None = ""
